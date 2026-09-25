import pytest
from fastapi.testclient import TestClient

from app.config import Settings
from app.container import AppContainer
from app.db.base import Base
from app.db.session import create_database
from app.main import create_app
from app.seed_data import seed_demo_content


class FakeEmbeddingService:
    model_name = "fake-embedding-model"

    @staticmethod
    def _embedding(text: str) -> list[float]:
        normalized = text.lower()
        return [
            1.0 if "equation" in normalized else 0.0,
            1.0 if "language" in normalized else 0.0,
            0.5,
        ]

    def embed_text(self, text: str) -> list[float]:
        return self._embedding(text)

    def embed_documents(self, documents: list[str]) -> list[list[float]]:
        return [self._embedding(document) for document in documents]


class FakeLLMService:
    def answer_question(self, question, chunks):
        return f"Grounded answer from chunk {chunks[0].position + 1}."


class FakeQuizService:
    def generate_questions(self, context, number=10):
        return [f"Question {index + 1}?" for index in range(number)]


@pytest.fixture
def client(tmp_path):
    settings = Settings(
        database_url=f"sqlite:///{tmp_path / 'test.db'}",
        gemini_api_key=None,
        retrieval_min_score=-1,
        chunk_size_words=50,
        chunk_overlap_words=10,
    )
    database = create_database(settings.database_url)
    Base.metadata.create_all(database.engine)
    with database.session_factory() as session:
        seed_demo_content(session)
    container = AppContainer(
        settings=settings,
        database=database,
        embedding_service=FakeEmbeddingService(),
        llm_service=FakeLLMService(),
        quiz_service=FakeQuizService(),
    )
    with TestClient(create_app(settings=settings, container=container)) as test_client:
        yield test_client
    database.engine.dispose()
