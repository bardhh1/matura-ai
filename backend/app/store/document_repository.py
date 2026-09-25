from __future__ import annotations

import uuid
from dataclasses import dataclass

import numpy as np
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.entities import Document, DocumentChunk


@dataclass(frozen=True)
class RetrievedChunk:
    id: uuid.UUID
    position: int
    content: str
    score: float


class DocumentRepository:
    """All document persistence and vector lookup live behind this boundary."""

    def __init__(self, session: Session):
        self.session = session

    def create(
        self,
        *,
        filename: str,
        content_type: str,
        size_bytes: int,
        embedding_model: str,
        chunks: list[str],
        embeddings: list[list[float]],
    ) -> Document:
        if len(chunks) != len(embeddings):
            raise ValueError("Every chunk must have exactly one embedding")

        document = Document(
            filename=filename,
            content_type=content_type,
            size_bytes=size_bytes,
            chunk_count=len(chunks),
            embedding_model=embedding_model,
        )
        document.chunks = [
            DocumentChunk(
                position=position,
                content=content,
                token_count=len(content.split()),
                embedding=embedding,
            )
            for position, (content, embedding) in enumerate(zip(chunks, embeddings, strict=True))
        ]
        self.session.add(document)
        try:
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise
        self.session.refresh(document)
        return document

    def get(self, document_id: uuid.UUID) -> Document | None:
        return self.session.get(Document, document_id)

    def list_documents(self, limit: int = 50) -> list[Document]:
        statement = select(Document).order_by(Document.created_at.desc()).limit(limit)
        return list(self.session.scalars(statement))

    def all_chunks(self, document_id: uuid.UUID) -> list[DocumentChunk]:
        statement = (
            select(DocumentChunk)
            .where(DocumentChunk.document_id == document_id)
            .order_by(DocumentChunk.position)
        )
        return list(self.session.scalars(statement))

    def search(
        self,
        *,
        document_id: uuid.UUID,
        query_embedding: list[float],
        top_k: int,
        min_score: float,
    ) -> list[RetrievedChunk]:
        if self.session.bind is not None and self.session.bind.dialect.name == "postgresql":
            distance = DocumentChunk.embedding.cosine_distance(query_embedding)
            statement = (
                select(DocumentChunk, distance.label("distance"))
                .where(DocumentChunk.document_id == document_id)
                .order_by(distance)
                .limit(top_k)
            )
            rows = self.session.execute(statement).all()
            return [
                RetrievedChunk(
                    id=chunk.id,
                    position=chunk.position,
                    content=chunk.content,
                    score=1.0 - float(distance_value),
                )
                for chunk, distance_value in rows
                if 1.0 - float(distance_value) >= min_score
            ]

        # SQLite is supported for tests and lightweight local work. Production uses pgvector.
        chunks = self.all_chunks(document_id)
        query = np.asarray(query_embedding, dtype=float)
        query_norm = np.linalg.norm(query)
        if query_norm == 0:
            return []

        results: list[RetrievedChunk] = []
        for chunk in chunks:
            embedding = np.asarray(chunk.embedding, dtype=float)
            denominator = np.linalg.norm(embedding) * query_norm
            score = float(np.dot(embedding, query) / denominator) if denominator else 0.0
            if score >= min_score:
                results.append(
                    RetrievedChunk(
                        id=chunk.id,
                        position=chunk.position,
                        content=chunk.content,
                        score=score,
                    )
                )

        return sorted(results, key=lambda item: item.score, reverse=True)[:top_k]
