import uuid
from datetime import UTC, datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.entities import (
    Attempt,
    Learner,
    LearningSession,
    Question,
    Skill,
    Subject,
    TutorInteraction,
)


class LearningRepository:
    def __init__(self, session: Session):
        self.session = session

    def list_subjects(self) -> list[Subject]:
        return list(self.session.scalars(select(Subject).order_by(Subject.sort_order)))

    def create_learner(self, display_name: str, locale: str, elective: str) -> Learner:
        learner = Learner(
            display_name=display_name.strip(),
            preferred_locale=locale,
            elective_subject_code=elective,
        )
        self.session.add(learner)
        self.session.commit()
        return learner

    def get_learner(self, learner_id: uuid.UUID) -> Learner | None:
        return self.session.get(Learner, learner_id)

    def update_learner(self, learner: Learner, locale: str | None, elective: str | None) -> Learner:
        if locale is not None:
            learner.preferred_locale = locale
        if elective is not None:
            learner.elective_subject_code = elective
        self.session.commit()
        return learner

    def track_subject_codes(self, learner: Learner) -> list[str]:
        return ["albanian", "mathematics", "english", learner.elective_subject_code]

    def list_track_skills(self, learner: Learner) -> list[tuple[Skill, Subject]]:
        codes = self.track_subject_codes(learner)
        statement = (
            select(Skill, Subject)
            .join(Subject, Subject.code == Skill.subject_code)
            .where(Skill.subject_code.in_(codes))
            .order_by(Subject.sort_order, Skill.sort_order, Skill.code)
        )
        return list(self.session.execute(statement).all())

    def diagnostic_questions(self, learner: Learner) -> list[Question]:
        codes = self.track_subject_codes(learner)
        statement = (
            select(Question)
            .join(Skill, Skill.code == Question.skill_code)
            .join(Subject, Subject.code == Skill.subject_code)
            .where(
                Skill.subject_code.in_(codes),
                Question.diagnostic_order.is_not(None),
                Question.is_active.is_(True),
            )
            .order_by(Subject.sort_order, Skill.sort_order, Question.diagnostic_order)
        )
        return list(self.session.scalars(statement))

    def practice_questions(self, skill_code: str, learner_id: uuid.UUID) -> list[Question]:
        attempted_ids = select(Attempt.question_id).where(Attempt.learner_id == learner_id)
        statement = (
            select(Question)
            .where(
                Question.skill_code == skill_code,
                Question.is_active.is_(True),
                Question.id.not_in(attempted_ids),
            )
            .order_by(Question.difficulty, Question.id)
            .limit(3)
        )
        questions = list(self.session.scalars(statement))
        if questions:
            return questions
        return list(
            self.session.scalars(
                select(Question)
                .where(Question.skill_code == skill_code, Question.is_active.is_(True))
                .order_by(Question.difficulty, Question.id)
                .limit(3)
            )
        )

    def create_session(
        self,
        learner_id: uuid.UUID,
        kind: str,
        questions: list[Question],
        target_skill_code: str | None = None,
    ) -> LearningSession:
        learning_session = LearningSession(
            learner_id=learner_id,
            kind=kind,
            target_skill_code=target_skill_code,
            question_ids=[str(question.id) for question in questions],
            status="active",
        )
        self.session.add(learning_session)
        self.session.commit()
        return learning_session

    def get_session(self, session_id: uuid.UUID) -> LearningSession | None:
        return self.session.get(LearningSession, session_id)

    def get_question(self, question_id: uuid.UUID) -> Question | None:
        return self.session.get(Question, question_id)

    def get_skill(self, skill_code: str) -> Skill | None:
        return self.session.get(Skill, skill_code)

    def get_subject(self, code: str) -> Subject | None:
        return self.session.get(Subject, code)

    def session_attempts(self, session_id: uuid.UUID) -> list[Attempt]:
        return list(
            self.session.scalars(
                select(Attempt).where(Attempt.session_id == session_id).order_by(Attempt.created_at)
            )
        )

    def learner_attempts(self, learner_id: uuid.UUID) -> list[tuple[Attempt, Question]]:
        return list(
            self.session.execute(
                select(Attempt, Question)
                .join(Question, Question.id == Attempt.question_id)
                .where(Attempt.learner_id == learner_id)
                .order_by(Attempt.created_at)
            ).all()
        )

    def add_attempt(
        self,
        learner_id: uuid.UUID,
        learning_session: LearningSession,
        question: Question,
        selected_index: int,
    ) -> Attempt:
        attempt = Attempt(
            learner_id=learner_id,
            session_id=learning_session.id,
            question_id=question.id,
            selected_index=selected_index,
            is_correct=selected_index == question.correct_index,
            weight=2 if learning_session.kind == "diagnostic" else 1,
        )
        self.session.add(attempt)
        self.session.flush()
        count = self.session.scalar(
            select(func.count(Attempt.id)).where(Attempt.session_id == learning_session.id)
        )
        if count >= len(learning_session.question_ids):
            learning_session.status = "completed"
            learning_session.completed_at = datetime.now(UTC)
        self.session.commit()
        return attempt

    def count_help(self, learner_id: uuid.UUID, question_id: uuid.UUID) -> int:
        return int(
            self.session.scalar(
                select(func.count(TutorInteraction.id)).where(
                    TutorInteraction.learner_id == learner_id,
                    TutorInteraction.question_id == question_id,
                )
            )
            or 0
        )

    def has_answered(self, learner_id: uuid.UUID, question_id: uuid.UUID) -> bool:
        return bool(
            self.session.scalar(
                select(func.count(Attempt.id)).where(
                    Attempt.learner_id == learner_id,
                    Attempt.question_id == question_id,
                )
            )
        )

    def add_tutor_interaction(
        self,
        learner_id: uuid.UUID,
        question_id: uuid.UUID,
        message: str,
        response: str,
        level: int,
        used_ai: bool,
    ) -> None:
        self.session.add(
            TutorInteraction(
                learner_id=learner_id,
                question_id=question_id,
                user_message=message,
                response=response,
                level=level,
                used_ai=used_ai,
            )
        )
        self.session.commit()
