import uuid

from app.errors import DocumentNotFoundError
from app.store.document_repository import DocumentRepository


class ChatHandler:
    def __init__(self, retrieval_service, llm_service, repository: DocumentRepository):
        self.retrieval_service = retrieval_service
        self.llm_service = llm_service
        self.repository = repository

    def ask(self, document_id: uuid.UUID, question: str):
        if self.repository.get(document_id) is None:
            raise DocumentNotFoundError("The selected document does not exist")

        results = self.retrieval_service.retrieve(document_id, question)

        if not results:
            return (
                "The uploaded material does not contain enough relevant information.",
                [],
            )

        return self.llm_service.answer_question(question, results), results
