from app.errors import ApplicationError
from app.services.generation_client import GenerationClient
from app.store.learning_repository import LearningRepository


class TutorService:
    def __init__(self, repository: LearningRepository, generation_client: GenerationClient | None):
        self.repository = repository
        self.generation_client = generation_client

    def help(self, learner, question, message: str) -> tuple[str, int, bool]:
        previous = self.repository.count_help(learner.id, question.id)
        answered = self.repository.has_answered(learner.id, question.id)
        level = 2 if answered or previous >= 1 else 1
        locale = learner.preferred_locale
        fallback = (
            question.hint_sq
            if locale == "sq" and level == 1
            else question.hint_en
            if level == 1
            else question.explanation_sq
            if locale == "sq"
            else question.explanation_en
        )
        language = "Albanian" if locale == "sq" else "English"
        mode = (
            "one short hint without revealing the answer"
            if level == 1
            else "a concise worked solution"
        )
        prompt = f"""
You are a patient Matura tutor. Reply in {language}.
Give {mode}. Use only the verified material below. Never change the correct answer.

QUESTION
{question.prompt_sq if locale == "sq" else question.prompt_en}

VERIFIED MATERIAL
{fallback}

STUDENT MESSAGE
{message}
""".strip()
        used_ai = False
        response = fallback
        try:
            if self.generation_client is None:
                raise RuntimeError("AI provider unavailable")
            generated = self.generation_client.generate(prompt, temperature=0.1)
            if generated.strip():
                response = generated.strip()
                used_ai = True
        except (ApplicationError, RuntimeError):
            pass
        self.repository.add_tutor_interaction(
            learner.id, question.id, message, response, level, used_ai
        )
        return response, level, used_ai
