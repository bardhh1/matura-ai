from typing import Annotated

from fastapi import APIRouter, File, UploadFile

from app.errors import UploadTooLargeError
from app.handlers.document_handler import DocumentHandler
from app.models.schemas import DocumentResponse, DocumentSummary
from app.store.document_repository import DocumentRepository


def create_document_router(container):
    router = APIRouter(prefix="/documents", tags=["Documents"])

    @router.post("/upload", response_model=DocumentResponse)
    def upload_document(file: Annotated[UploadFile, File()]):
        content = file.file.read(container.settings.max_upload_bytes + 1)
        if len(content) > container.settings.max_upload_bytes:
            raise UploadTooLargeError(
                f"Files must be smaller than {container.settings.max_upload_bytes // 1024 // 1024} MB"
            )

        with container.database.session_factory() as session:
            handler = DocumentHandler(
                container.embedding_service,
                DocumentRepository(session),
                chunk_size_words=container.settings.chunk_size_words,
                chunk_overlap_words=container.settings.chunk_overlap_words,
            )
            document = handler.process_document(
                filename=file.filename or "document",
                content_type=file.content_type or "application/octet-stream",
                content=content,
            )
            return DocumentResponse(
                id=document.id,
                filename=document.filename,
                message="Document processed successfully.",
                chunks=document.chunk_count,
            )

    @router.get("/", response_model=list[DocumentSummary])
    def list_documents():
        with container.database.session_factory() as session:
            documents = DocumentRepository(session).list_documents()
            return [
                DocumentSummary(
                    id=document.id,
                    filename=document.filename,
                    content_type=document.content_type,
                    size_bytes=document.size_bytes,
                    chunks=document.chunk_count,
                    created_at=document.created_at,
                )
                for document in documents
            ]

    return router
