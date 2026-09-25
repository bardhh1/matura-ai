from sentence_transformers import SentenceTransformer


class EmbeddingService:

    def __init__(self):
        # Local embedding model.
        # No API key is required for this model.
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def embed_text(self, text: str):
        """
        Convert one piece of text into an embedding vector.
        """

        return self.model.encode(text)

    def embed_documents(self, documents: list[str]):
        """
        Convert multiple document chunks into embedding vectors.
        """

        return self.model.encode(documents)