from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.services.embedding_service import EmbeddingService
from app.services.retrieval_service import RetrievalService
from app.services.llm_service import LLMService
from app.services.quiz_service import QuizService

from app.store.vector_store import VectorStore

from app.handlers.document_handler import DocumentHandler
from app.handlers.chat_handler import ChatHandler
from app.handlers.quiz_handler import QuizHandler

from app.routes.document_routes import create_document_router
from app.routes.chat_routes import create_chat_router
from app.routes.quiz_routes import create_quiz_router


# --------------------------------------------------
# Create FastAPI application
# --------------------------------------------------

app = FastAPI(
    title="AI Document Assistant",
    description="RAG-based document question answering system",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --------------------------------------------------
# Create services
# --------------------------------------------------

embedding_service = EmbeddingService()

vector_store = VectorStore()

retrieval_service = RetrievalService(
    embedding_service,
    vector_store
)

llm_service = LLMService()

quiz_service = QuizService()


# --------------------------------------------------
# Create handlers
# --------------------------------------------------

document_handler = DocumentHandler(
    embedding_service,
    vector_store
)

chat_handler = ChatHandler(
    retrieval_service,
    llm_service
)

quiz_handler = QuizHandler(
    vector_store,
    quiz_service
)


# --------------------------------------------------
# Register routes
# --------------------------------------------------

app.include_router(
    create_document_router(document_handler)
)

app.include_router(
    create_chat_router(chat_handler)
)

app.include_router(
    create_quiz_router(quiz_handler)
)


# --------------------------------------------------
# Basic test endpoint
# --------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "AI Document Assistant API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }