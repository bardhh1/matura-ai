import uuid

from app.store.document_repository import DocumentRepository, RetrievedChunk


class RetrievalService:
    def __init__(
        self,
        embedding_service,
        repository: DocumentRepository,
        *,
        top_k: int,
        min_score: float,
    ):
        self.embedding_service = embedding_service
        self.repository = repository
        self.top_k = top_k
        self.min_score = min_score

    def retrieve(self, document_id: uuid.UUID, question: str) -> list[RetrievedChunk]:
        question_embedding = self.embedding_service.embed_text(question)
        return self.repository.search(
            document_id=document_id,
            query_embedding=question_embedding,
            top_k=self.top_k,
            min_score=self.min_score,
        )
