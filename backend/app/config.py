from functools import lru_cache
from typing import Annotated, Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration loaded from environment variables or backend/.env."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "Matura AI API"
    app_env: str = "development"
    api_prefix: str = "/api/v1"
    database_url: str = "postgresql+psycopg://matura:matura@localhost:5432/matura"

    llm_provider: Literal["gemini", "openrouter"] = "gemini"
    gemini_api_key: str | None = None
    gemini_model: str = "gemini-2.5-flash"
    openrouter_api_key: str | None = None
    openrouter_model: str = "google/gemma-3-27b-it"
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    openrouter_site_url: str | None = None
    openrouter_app_name: str = "Matura AI"
    embedding_model: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    embedding_dimension: int = 384

    retrieval_top_k: int = Field(default=5, ge=1, le=20)
    retrieval_min_score: float = Field(default=0.25, ge=-1.0, le=1.0)
    chunk_size_words: int = Field(default=120, ge=50, le=1000)
    chunk_overlap_words: int = Field(default=20, ge=0, le=250)
    max_upload_bytes: int = Field(default=15 * 1024 * 1024, ge=1024)
    max_quiz_context_chars: int = Field(default=60_000, ge=1_000)
    allowed_origins: Annotated[list[str], NoDecode] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

    @field_validator("allowed_origins", mode="before")
    @classmethod
    def parse_allowed_origins(cls, value):
        if isinstance(value, str) and not value.lstrip().startswith("["):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value

    @field_validator("chunk_overlap_words")
    @classmethod
    def overlap_must_be_smaller_than_chunk(cls, value: int, info):
        chunk_size = info.data.get("chunk_size_words", 300)
        if value >= chunk_size:
            raise ValueError("chunk_overlap_words must be smaller than chunk_size_words")
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()
