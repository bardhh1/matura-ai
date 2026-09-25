import uuid
from dataclasses import dataclass

from app.errors import (
    InvalidLearningStateError,
    LearnerNotFoundError,
    LearningSessionNotFoundError,
    QuestionNotFoundError,
)
from app.store.learning_repository import LearningRepository


@dataclass(frozen=True)
class Mastery:
    score: int | None
    attempts: int


class LearningService:
    def __init__(self, repository: LearningRepository):
        self.repository = repository

    @staticmethod
    def mastery_for(attempts) -> Mastery:
        if not attempts:
            return Mastery(score=None, attempts=0)
        weighted_correct = sum(item.weight for item in attempts if item.is_correct)
        weighted_attempts = sum(item.weight for item in attempts)
        score = round(100 * (1 + weighted_correct) / (2 + weighted_attempts))
        return Mastery(score=score, attempts=len(attempts))

    def learner_or_error(self, learner_id: uuid.UUID):
        learner = self.repository.get_learner(learner_id)
        if not learner:
            raise LearnerNotFoundError("Learner profile was not found")
        return learner

    def mastery_map(self, learner_id: uuid.UUID):
        learner = self.learner_or_error(learner_id)
        attempts_by_skill: dict[str, list] = {}
        all_attempts = self.repository.learner_attempts(learner_id)
        for attempt, question in all_attempts:
            attempts_by_skill.setdefault(question.skill_code, []).append(attempt)

        subjects: dict[str, dict] = {}
        weakest = None
        for skill, subject in self.repository.list_track_skills(learner):
            mastery = self.mastery_for(attempts_by_skill.get(skill.code, []))
            item = {"skill": skill, "mastery": mastery}
            subjects.setdefault(subject.code, {"subject": subject, "skills": []})["skills"].append(
                item
            )
            rank = (
                mastery.score if mastery.score is not None else -1,
                mastery.attempts,
                skill.code,
            )
            if weakest is None or rank < weakest[0]:
                weakest = (rank, item)

        completed_diagnostic = (
            any(attempt.weight == 2 for attempt, _question in all_attempts)
            and sum(1 for attempt, _question in all_attempts if attempt.weight == 2) >= 12
        )
        return (
            learner,
            list(subjects.values()),
            weakest[1] if weakest else None,
            len(all_attempts),
            completed_diagnostic,
        )

    def start_diagnostic(self, learner_id: uuid.UUID):
        learner = self.learner_or_error(learner_id)
        questions = self.repository.diagnostic_questions(learner)
        if len(questions) != 12:
            raise InvalidLearningStateError(
                "The diagnostic bank is incomplete. Run the seed command."
            )
        return self.repository.create_session(learner_id, "diagnostic", questions)

    def start_practice(self, learner_id: uuid.UUID):
        _learner, _subjects, weakest, _total, diagnostic_complete = self.mastery_map(learner_id)
        if not diagnostic_complete:
            raise InvalidLearningStateError("Complete the diagnostic before starting practice")
        questions = self.repository.practice_questions(weakest["skill"].code, learner_id)
        if not questions:
            raise InvalidLearningStateError("No practice questions are available")
        return self.repository.create_session(
            learner_id, "practice", questions, target_skill_code=weakest["skill"].code
        )

    def next_question(self, session_id: uuid.UUID):
        learning_session = self.repository.get_session(session_id)
        if not learning_session:
            raise LearningSessionNotFoundError("Learning session was not found")
        attempted = {str(item.question_id) for item in self.repository.session_attempts(session_id)}
        for position, raw_id in enumerate(learning_session.question_ids, start=1):
            if raw_id not in attempted:
                question = self.repository.get_question(uuid.UUID(raw_id))
                if question:
                    return learning_session, question, position
        return learning_session, None, len(learning_session.question_ids)

    def answer(self, session_id: uuid.UUID, question_id: uuid.UUID, selected_index: int):
        learning_session = self.repository.get_session(session_id)
        if not learning_session:
            raise LearningSessionNotFoundError("Learning session was not found")
        if str(question_id) not in learning_session.question_ids:
            raise InvalidLearningStateError("Question does not belong to this session")
        question = self.repository.get_question(question_id)
        if not question:
            raise QuestionNotFoundError("Question was not found")
        skill_attempts = [
            attempt
            for attempt, attempted_question in self.repository.learner_attempts(
                learning_session.learner_id
            )
            if attempted_question.skill_code == question.skill_code
        ]
        before = self.mastery_for(skill_attempts)
        attempt = self.repository.add_attempt(
            learning_session.learner_id, learning_session, question, selected_index
        )
        after = self.mastery_for([*skill_attempts, attempt])
        return learning_session, question, attempt, before, after
