from fastapi import APIRouter

from app.models.schemas import QuizRequest, QuizResponse


def create_quiz_router(quiz_handler):

    router = APIRouter(
        prefix="/quiz",
        tags=["Quiz"]
    )

    @router.post(
        "/generate",
        response_model=QuizResponse
    )
    async def generate_quiz(request: QuizRequest):

        questions = quiz_handler.generate_quiz(
            request.number
        )

        return QuizResponse(
            questions=questions
        )

    return router