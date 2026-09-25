from dataclasses import dataclass

from app.config import Settings
from app.db.session import Database, create_database
from app.services.embedding_service import EmbeddingService
from app.services.generation_client import create_generation_client
from app.services.llm_service import LLMService
from app.services.quiz_service import QuizService


@dataclass(frozen=True)
class AppContainer:
    settings: Settings
    database: Database
    embedding_service: EmbeddingService
    llm_service: LLMService
    quiz_service: QuizService
    generation_client: object | None = None


def create_container(settings: Settings) -> AppContainer:
    generation_client = create_generation_client(settings)
    return AppContainer(
        settings=settings,
        database=create_database(settings.database_url),
        embedding_service=EmbeddingService(
            settings.embedding_model,
            expected_dimension=settings.embedding_dimension,
        ),
        llm_service=LLMService(generation_client),
        quiz_service=QuizService(generation_client),
        generation_client=generation_client,
    )
