import uuid

from app.errors import DocumentNotFoundError
from app.store.document_repository import DocumentRepository


class QuizHandler:
    def __init__(
        self,
        repository: DocumentRepository,
        quiz_service,
        *,
        max_context_chars: int,
    ):
        self.repository = repository
        self.quiz_service = quiz_service
        self.max_context_chars = max_context_chars

    def generate_quiz(self, document_id: uuid.UUID, number: int = 10):
        if self.repository.get(document_id) is None:
            raise DocumentNotFoundError("The selected document does not exist")

        chunks = self.repository.all_chunks(document_id)
        context = "\n\n".join(chunk.content for chunk in chunks)[: self.max_context_chars]
        return self.quiz_service.generate_questions(context, number)
