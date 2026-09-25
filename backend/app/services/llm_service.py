import google.generativeai as genai

from app.config import GEMINI_API_KEY, GEMINI_MODEL


class LLMService:

    def __init__(self):

        genai.configure(api_key=GEMINI_API_KEY)

        self.model = genai.GenerativeModel(
            model_name=GEMINI_MODEL,
            generation_config={
                "temperature": 0
            }
        )

    def check_coverage(self, question: str, context: str) -> str:
        """
        Check whether the document contains enough information
        to answer the question.
        """

        prompt = f"""
You are checking whether a document contains enough information
to answer a question.

Document:
{context}

Question:
{question}

Return exactly one of these:

Yes
Partial
No

Rules:

Yes = the document contains enough information to answer the
question completely.

Partial = the document contains some information but not enough
to answer everything.

No = the document does not contain the information needed.
"""

        response = self.model.generate_content(prompt)

        return response.text.strip()

    def answer_question(self, question: str, context: str) -> str:
        """
        Answer the question using only the supplied document context.
        """

        coverage = self.check_coverage(question, context)

        if coverage == "No":
            return "I don't know — not found in the document."

        prompt = f"""
You are a document-based AI assistant.

Answer the user's question using ONLY the information
contained in the document context below.

Do not use outside knowledge.

If the information is incomplete, clearly say that the
document does not provide enough information.

Document context:
{context}

User question:
{question}

Answer:
"""

        response = self.model.generate_content(prompt)

        return response.text.strip()