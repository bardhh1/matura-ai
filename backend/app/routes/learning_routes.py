import uuid

from fastapi import APIRouter, Query

from app.errors import InvalidLearningStateError, QuestionNotFoundError
from app.models.schemas import (
    AnswerRequest,
    AnswerResponse,
    CatalogResponse,
    DashboardResponse,
    LearnerCreate,
    LearnerResponse,
    LearnerUpdate,
    NextQuestionResponse,
    QuestionResponse,
    SessionResponse,
    SkillMasteryResponse,
    SubjectMasteryResponse,
    SubjectResponse,
    TutorHelpRequest,
    TutorHelpResponse,
)
from app.services.learning_service import LearningService
from app.services.tutor_service import TutorService
from app.store.learning_repository import LearningRepository


def localized(entity, field: str, locale: str):
    return getattr(entity, f"{field}_{locale}")


def session_payload(learning_session, completed: int) -> SessionResponse:
    return SessionResponse(
        id=learning_session.id,
        kind=learning_session.kind,
        total_questions=len(learning_session.question_ids),
        completed_questions=completed,
        target_skill_code=learning_session.target_skill_code,
    )


def create_learning_router(container, generation_client):
    router = APIRouter(tags=["Adaptive learning"])

    @router.get("/catalog/subjects", response_model=CatalogResponse)
    def catalog(locale: str = Query(default="sq", pattern="^(sq|en)$")):
        with container.database.session_factory() as db:
            subjects = LearningRepository(db).list_subjects()
            mapped = [
                SubjectResponse(
                    code=item.code,
                    name=localized(item, "name", locale),
                    is_core=item.is_core,
                )
                for item in subjects
            ]
            return CatalogResponse(
                core=[item for item in mapped if item.is_core],
                electives=[item for item in mapped if not item.is_core],
            )

    @router.post("/learners", response_model=LearnerResponse)
    def create_learner(payload: LearnerCreate):
        with container.database.session_factory() as db:
            repository = LearningRepository(db)
            subject = repository.get_subject(payload.elective_subject_code)
            if not subject or subject.is_core:
                raise InvalidLearningStateError("Select a valid elective subject")
            learner = repository.create_learner(
                payload.display_name, payload.preferred_locale, payload.elective_subject_code
            )
            return LearnerResponse.model_validate(learner, from_attributes=True)

    @router.post("/demo/learners", response_model=LearnerResponse)
    def create_demo_learner():
        """Create a fresh, pre-diagnosed profile for a short judge walkthrough."""
        with container.database.session_factory() as db:
            repository = LearningRepository(db)
            service = LearningService(repository)
            learner = repository.create_learner("Arta Demo", "sq", "history")
            learning_session = service.start_diagnostic(learner.id)
            for raw_id in learning_session.question_ids:
                question = repository.get_question(uuid.UUID(raw_id))
                selected = question.correct_index
                if question.skill_code in {"math_algebra", "math_geometry"}:
                    selected = (question.correct_index + 1) % 4
                repository.add_attempt(learner.id, learning_session, question, selected)
            return LearnerResponse.model_validate(learner, from_attributes=True)

    @router.patch("/learners/{learner_id}", response_model=LearnerResponse)
    def update_learner(learner_id: uuid.UUID, payload: LearnerUpdate):
        with container.database.session_factory() as db:
            repository = LearningRepository(db)
            service = LearningService(repository)
            learner = service.learner_or_error(learner_id)
            if payload.elective_subject_code:
                subject = repository.get_subject(payload.elective_subject_code)
                if not subject or subject.is_core:
                    raise InvalidLearningStateError("Select a valid elective subject")
            learner = repository.update_learner(
                learner, payload.preferred_locale, payload.elective_subject_code
            )
            return LearnerResponse.model_validate(learner, from_attributes=True)

    @router.get("/learners/{learner_id}/dashboard", response_model=DashboardResponse)
    def dashboard(learner_id: uuid.UUID):
        with container.database.session_factory() as db:
            repository = LearningRepository(db)
            learner, groups, weakest, total, diagnostic_complete = LearningService(
                repository
            ).mastery_map(learner_id)
            locale = learner.preferred_locale
            subject_payloads = []
            for group in groups:
                skills = [
                    SkillMasteryResponse(
                        code=item["skill"].code,
                        name=localized(item["skill"], "name", locale),
                        score=item["mastery"].score,
                        attempts=item["mastery"].attempts,
                    )
                    for item in group["skills"]
                ]
                measured = [skill.score for skill in skills if skill.score is not None]
                subject_payloads.append(
                    SubjectMasteryResponse(
                        code=group["subject"].code,
                        name=localized(group["subject"], "name", locale),
                        score=round(sum(measured) / len(measured)) if measured else None,
                        skills=skills,
                    )
                )
            weakest_payload = None
            if weakest:
                weakest_payload = SkillMasteryResponse(
                    code=weakest["skill"].code,
                    name=localized(weakest["skill"], "name", locale),
                    score=weakest["mastery"].score,
                    attempts=weakest["mastery"].attempts,
                )
            return DashboardResponse(
                learner=LearnerResponse.model_validate(learner, from_attributes=True),
                diagnostic_complete=diagnostic_complete,
                subjects=subject_payloads,
                weakest_skill=weakest_payload,
                total_attempts=total,
            )

    @router.post("/learners/{learner_id}/diagnostics", response_model=SessionResponse)
    def start_diagnostic(learner_id: uuid.UUID):
        with container.database.session_factory() as db:
            learning_session = LearningService(LearningRepository(db)).start_diagnostic(learner_id)
            return session_payload(learning_session, 0)

    @router.post("/learners/{learner_id}/practice", response_model=SessionResponse)
    def start_practice(learner_id: uuid.UUID):
        with container.database.session_factory() as db:
            learning_session = LearningService(LearningRepository(db)).start_practice(learner_id)
            return session_payload(learning_session, 0)

    @router.get("/sessions/{session_id}/next", response_model=NextQuestionResponse)
    def next_question(session_id: uuid.UUID):
        with container.database.session_factory() as db:
            repository = LearningRepository(db)
            service = LearningService(repository)
            learning_session, question, position = service.next_question(session_id)
            learner = service.learner_or_error(learning_session.learner_id)
            attempts = repository.session_attempts(session_id)
            question_payload = None
            if question:
                skill = repository.get_skill(question.skill_code)
                subject = repository.get_subject(skill.subject_code)
                locale = learner.preferred_locale
                question_payload = QuestionResponse(
                    id=question.id,
                    session_id=learning_session.id,
                    position=position,
                    total=len(learning_session.question_ids),
                    subject=localized(subject, "name", locale),
                    skill=localized(skill, "name", locale),
                    prompt=localized(question, "prompt", locale),
                    options=localized(question, "options", locale),
                    difficulty=question.difficulty,
                    source_label=question.source_label,
                )
            return NextQuestionResponse(
                session=session_payload(learning_session, len(attempts)), question=question_payload
            )

    @router.post("/sessions/{session_id}/answers", response_model=AnswerResponse)
    def answer(session_id: uuid.UUID, payload: AnswerRequest):
        with container.database.session_factory() as db:
            repository = LearningRepository(db)
            service = LearningService(repository)
            learning_session, question, attempt, before, after = service.answer(
                session_id, payload.question_id, payload.selected_index
            )
            learner = service.learner_or_error(learning_session.learner_id)
            locale = learner.preferred_locale
            return AnswerResponse(
                correct=attempt.is_correct,
                correct_index=question.correct_index,
                feedback=("Saktë!" if locale == "sq" else "Correct!")
                if attempt.is_correct
                else (
                    "Jo ende. Shiko shpjegimin."
                    if locale == "sq"
                    else "Not yet. Review the explanation."
                ),
                explanation=localized(question, "explanation", locale),
                source_label=question.source_label,
                mastery_before=before.score,
                mastery_after=after.score,
                session_complete=learning_session.status == "completed",
                next_action="dashboard"
                if learning_session.status == "completed"
                else "next_question",
            )

    @router.post("/tutor/help", response_model=TutorHelpResponse)
    def tutor_help(payload: TutorHelpRequest):
        with container.database.session_factory() as db:
            repository = LearningRepository(db)
            service = LearningService(repository)
            learner = service.learner_or_error(payload.learner_id)
            question = repository.get_question(payload.question_id)
            if not question:
                raise QuestionNotFoundError("Question was not found")
            response, level, used_ai = TutorService(repository, generation_client).help(
                learner, question, payload.message
            )
            return TutorHelpResponse(response=response, level=level, used_ai=used_ai)

    return router
