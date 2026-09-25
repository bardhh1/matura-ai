from app.config import TOP_K


class RetrievalService:

    def __init__(self, embedding_service, vector_store):
        self.embedding_service = embedding_service
        self.vector_store = vector_store

    def retrieve(self, question: str, top_k: int = TOP_K):
        """
        Retrieve the most relevant document chunks for a question.
        """

        # Convert question into an embedding
        question_embedding = self.embedding_service.embed_text(question)

        # Search the vector store
        results = self.vector_store.search(
            question_embedding,
            top_k
        )

        return results