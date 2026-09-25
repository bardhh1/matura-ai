class ChatHandler:

    def __init__(self, retrieval_service, llm_service):
        self.retrieval_service = retrieval_service
        self.llm_service = llm_service

    def ask(self, question: str):

        # Retrieve relevant chunks
        results = self.retrieval_service.retrieve(question)

        if not results:
            return "I don't know — not found in the document."

        # Extract the text from the results
        context_parts = []

        for result in results:
            context_parts.append(result["text"])

        # Combine retrieved chunks
        context = "\n\n".join(context_parts)

        # Ask Gemini using only those chunks
        answer = self.llm_service.answer_question(
            question,
            context
        )

        return answer