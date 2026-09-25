from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.config import Settings, get_settings
from app.container import AppContainer, create_container
from app.errors import ApplicationError
from app.routes.chat_routes import create_chat_router
from app.routes.document_routes import create_document_router
from app.routes.learning_routes import create_learning_router
from app.routes.quiz_routes import create_quiz_router


def create_app(
    settings: Settings | None = None,
    container: AppContainer | None = None,
) -> FastAPI:
    settings = settings or get_settings()
    container = container or create_container(settings)

    application = FastAPI(
        title=settings.app_name,
        description="Document-grounded learning API for Matura students",
        version="2.1.0",
    )
    application.state.container = container
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @application.exception_handler(ApplicationError)
    async def handle_application_error(_request: Request, exc: ApplicationError):
        return JSONResponse(
            status_code=exc.status_code,
            content={"code": exc.code, "detail": str(exc)},
        )

    @application.exception_handler(SQLAlchemyError)
    async def handle_database_error(_request: Request, _exc: SQLAlchemyError):
        return JSONResponse(
            status_code=503,
            content={
                "code": "database_unavailable",
                "detail": "The database is unavailable. Start PostgreSQL and run migrations.",
            },
        )

    application.include_router(create_document_router(container), prefix=settings.api_prefix)
    application.include_router(create_chat_router(container), prefix=settings.api_prefix)
    application.include_router(create_quiz_router(container), prefix=settings.api_prefix)
    application.include_router(
        create_learning_router(
            container,
            container.generation_client
            or getattr(container.llm_service, "generation_client", None),
        ),
        prefix=settings.api_prefix,
    )

    @application.get("/")
    def root():
        return {"message": "Matura AI API is running", "docs": "/docs"}

    @application.get("/health/live")
    def liveness():
        return {"status": "healthy"}

    @application.get("/health/ready")
    def readiness():
        with container.database.session_factory() as session:
            session.execute(text("SELECT 1"))
        return {"status": "ready"}

    @application.get("/health/providers")
    def provider_status():
        provider = settings.llm_provider
        configured = bool(
            settings.openrouter_api_key if provider == "openrouter" else settings.gemini_api_key
        )
        return {"provider": provider, "configured": configured}

    @application.get("/health", include_in_schema=False)
    def legacy_health():
        return liveness()

    return application


app = create_app()
