from fastapi import APIRouter

from app.models.schemas import ChatRequest, ChatResponse


def create_chat_router(chat_handler):

    router = APIRouter(
        prefix="/chat",
        tags=["Chat"]
    )

    @router.post(
        "/",
        response_model=ChatResponse
    )
    async def chat(request: ChatRequest):

        answer = chat_handler.ask(
            request.question
        )

        return ChatResponse(
            answer=answer
        )

    return router