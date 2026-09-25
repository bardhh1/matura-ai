from fastapi import APIRouter, UploadFile, File

import tempfile
import os

from app.models.schemas import DocumentResponse


router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


def create_document_router(document_handler):

    router = APIRouter(
        prefix="/documents",
        tags=["Documents"]
    )

    @router.post(
        "/upload",
        response_model=DocumentResponse
    )
    async def upload_document(
        file: UploadFile = File(...)
    ):

        # Create temporary file
        suffix = os.path.splitext(file.filename)[1]

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix
        ) as temp_file:

            content = await file.read()

            temp_file.write(content)

            temp_path = temp_file.name

        try:

            result = document_handler.process_document(
                temp_path
            )

            return result

        finally:

            # Delete temporary file
            if os.path.exists(temp_path):
                os.remove(temp_path)

    return router