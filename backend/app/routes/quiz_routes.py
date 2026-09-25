from fastapi import APIRouter

from app.handlers.quiz_handler import QuizHandler
from app.models.schemas import QuizRequest, QuizResponse
from app.store.document_repository import DocumentRepository


def create_quiz_router(container):

    router = APIRouter(prefix="/quiz", tags=["Quiz"])

    @router.post("/generate", response_model=QuizResponse)
    def generate_quiz(request: QuizRequest):
        with container.database.session_factory() as session:
            handler = QuizHandler(
                DocumentRepository(session),
                container.quiz_service,
                max_context_chars=container.settings.max_quiz_context_chars,
            )
            questions = handler.generate_quiz(request.document_id, request.number)
            return QuizResponse(questions=questions)

    return router
