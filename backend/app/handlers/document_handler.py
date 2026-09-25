from pathlib import Path

from app.services.document_service import chunk_text, extract_text
from app.store.document_repository import DocumentRepository


class DocumentHandler:
    def __init__(
        self,
        embedding_service,
        repository: DocumentRepository,
        *,
        chunk_size_words: int,
        chunk_overlap_words: int,
    ):
        self.embedding_service = embedding_service
        self.repository = repository
        self.chunk_size_words = chunk_size_words
        self.chunk_overlap_words = chunk_overlap_words

    def process_document(self, *, filename: str, content_type: str, content: bytes):
        safe_filename = Path(filename).name or "document"
        text = extract_text(safe_filename, content)
        chunks = chunk_text(
            text,
            target_words=self.chunk_size_words,
            overlap_words=self.chunk_overlap_words,
        )
        embeddings = self.embedding_service.embed_documents(chunks)
        return self.repository.create(
            filename=safe_filename,
            content_type=content_type or "application/octet-stream",
            size_bytes=len(content),
            embedding_model=self.embedding_service.model_name,
            chunks=chunks,
            embeddings=embeddings,
        )
