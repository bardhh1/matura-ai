class QuizHandler:

    def __init__(self, vector_store, quiz_service):
        self.vector_store = vector_store
        self.quiz_service = quiz_service

    def generate_quiz(self, number: int = 10):

        if not self.vector_store.documents:
            raise ValueError("No document has been loaded.")

        # Use all document chunks for quiz generation
        context = "\n\n".join(
            self.vector_store.documents
        )

        questions = self.quiz_service.generate_questions(
            context,
            number
        )

        return questions