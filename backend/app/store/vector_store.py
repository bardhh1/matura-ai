import numpy as np


class VectorStore:

    def __init__(self):
        self.documents = []
        self.embeddings = []

    def add_documents(self, documents, embeddings):
        """
        Store document chunks and their embeddings.
        """

        self.documents = documents
        self.embeddings = np.array(embeddings)

    def search(self, query_embedding, top_k=3):
        """
        Find the most similar document chunks.
        """

        if len(self.documents) == 0:
            return []

        query = np.array(query_embedding)

        # Calculate cosine similarity
        similarities = np.dot(self.embeddings, query) / (
            np.linalg.norm(self.embeddings, axis=1)
            * np.linalg.norm(query)
        )

        # Get indexes of the highest scores
        top_indexes = np.argsort(similarities)[::-1][:top_k]

        results = []

        for index in top_indexes:
            results.append({
                "text": self.documents[index],
                "score": float(similarities[index])
            })

        return results