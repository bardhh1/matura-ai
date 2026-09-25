from app.services.document_service import load_document, chunk_text


class DocumentHandler:

    def __init__(self, embedding_service, vector_store):
        self.embedding_service = embedding_service
        self.vector_store = vector_store

    def process_document(self, file_path: str):

        # Load document
        text = load_document(file_path)

        # Split document into chunks
        chunks = chunk_text(text)

        if not chunks:
            raise ValueError("Document does not contain any text.")

        # Create embeddings
        embeddings = self.embedding_service.embed_documents(chunks)

        # Save chunks and embeddings
        self.vector_store.add_documents(
            chunks,
            embeddings
        )

        return {
            "message": "Document processed successfully.",
            "chunks": len(chunks)
        }