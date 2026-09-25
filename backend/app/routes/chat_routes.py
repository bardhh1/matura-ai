from fastapi import APIRouter

from app.handlers.chat_handler import ChatHandler
from app.models.schemas import ChatRequest, ChatResponse, SourceResponse
from app.services.retrieval_service import RetrievalService
from app.store.document_repository import DocumentRepository


def create_chat_router(container):

    router = APIRouter(prefix="/chat", tags=["Chat"])

    @router.post("/", response_model=ChatResponse)
    def chat(request: ChatRequest):
        with container.database.session_factory() as session:
            repository = DocumentRepository(session)
            retrieval_service = RetrievalService(
                container.embedding_service,
                repository,
                top_k=container.settings.retrieval_top_k,
                min_score=container.settings.retrieval_min_score,
            )
            handler = ChatHandler(retrieval_service, container.llm_service, repository)
            answer, chunks = handler.ask(request.document_id, request.question)
            return ChatResponse(
                answer=answer,
                sources=[
                    SourceResponse(
                        chunk=chunk.position + 1,
                        excerpt=chunk.content[:240],
                        score=round(chunk.score, 4),
                    )
                    for chunk in chunks
                ],
            )

    return router
