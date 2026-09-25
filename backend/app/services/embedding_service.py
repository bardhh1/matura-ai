from sentence_transformers import SentenceTransformer


class EmbeddingService:
    def __init__(self, model_name: str, expected_dimension: int = 384):
        self.model_name = model_name
        self.expected_dimension = expected_dimension
        self._model: SentenceTransformer | None = None

    @property
    def model(self) -> SentenceTransformer:
        if self._model is None:
            self._model = SentenceTransformer(self.model_name)
        return self._model

    def embed_text(self, text: str):
        """
        Convert one piece of text into an embedding vector.
        """

        embedding = self.model.encode(text, normalize_embeddings=True).tolist()
        self._validate_dimension(embedding)
        return embedding

    def embed_documents(self, documents: list[str]):
        """
        Convert multiple document chunks into embedding vectors.
        """

        embeddings = self.model.encode(documents, normalize_embeddings=True).tolist()
        for embedding in embeddings:
            self._validate_dimension(embedding)
        return embeddings

    def _validate_dimension(self, embedding: list[float]) -> None:
        if len(embedding) != self.expected_dimension:
            raise ValueError(
                f"Embedding model returned {len(embedding)} dimensions; "
                f"the database expects {self.expected_dimension}"
            )
