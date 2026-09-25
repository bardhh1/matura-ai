import google.generativeai as genai

from app.config import GEMINI_API_KEY, GEMINI_MODEL


class QuizService:

    def __init__(self):

        genai.configure(api_key=GEMINI_API_KEY)

        self.model = genai.GenerativeModel(
            model_name=GEMINI_MODEL,
            generation_config={
                "temperature": 0.2
            }
        )

    def generate_questions(self, context: str, number: int = 10):
        """
        Generate quiz questions using only the document.
        """

        prompt = f"""
Create {number} study questions based ONLY on the document below.

Do not use information outside the document.

Document:
{context}

Return one question per line.

Do not number the questions.
"""

        response = self.model.generate_content(prompt)

        lines = response.text.split("\n")

        questions = []

        for line in lines:
            line = line.strip()

            if not line:
                continue

            # Remove common numbering
            if line[0].isdigit():
                line = line.lstrip("0123456789. ")

            questions.append(line)

        return questions[:number]