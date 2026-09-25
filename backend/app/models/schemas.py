import uuid
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    document_id: uuid.UUID
    question: str = Field(min_length=2, max_length=2_000)


class SourceResponse(BaseModel):
    chunk: int
    excerpt: str
    score: float


class ChatResponse(BaseModel):
    answer: str
    sources: list[SourceResponse]


class QuizRequest(BaseModel):
    document_id: uuid.UUID
    number: int = Field(default=10, ge=1, le=30)


class QuizResponse(BaseModel):
    questions: list[str]


class DocumentResponse(BaseModel):
    id: uuid.UUID
    filename: str
    message: str
    chunks: int


class DocumentSummary(BaseModel):
    id: uuid.UUID
    filename: str
    content_type: str
    size_bytes: int
    chunks: int
    created_at: datetime


class ErrorResponse(BaseModel):
    code: str
    detail: str


Locale = Literal["sq", "en"]
ElectiveCode = Literal["history", "biology", "informatics"]


class SubjectResponse(BaseModel):
    code: str
    name: str
    is_core: bool


class CatalogResponse(BaseModel):
    core: list[SubjectResponse]
    electives: list[SubjectResponse]


class LearnerCreate(BaseModel):
    display_name: str = Field(min_length=2, max_length=80)
    preferred_locale: Locale = "sq"
    elective_subject_code: ElectiveCode


class LearnerUpdate(BaseModel):
    preferred_locale: Locale | None = None
    elective_subject_code: ElectiveCode | None = None


class LearnerResponse(BaseModel):
    id: uuid.UUID
    display_name: str
    preferred_locale: Locale
    elective_subject_code: str


class SkillMasteryResponse(BaseModel):
    code: str
    name: str
    score: int | None
    attempts: int


class SubjectMasteryResponse(BaseModel):
    code: str
    name: str
    score: int | None
    skills: list[SkillMasteryResponse]


class DashboardResponse(BaseModel):
    learner: LearnerResponse
    diagnostic_complete: bool
    subjects: list[SubjectMasteryResponse]
    weakest_skill: SkillMasteryResponse | None
    total_attempts: int


class SessionResponse(BaseModel):
    id: uuid.UUID
    kind: str
    total_questions: int
    completed_questions: int
    target_skill_code: str | None


class QuestionResponse(BaseModel):
    id: uuid.UUID
    session_id: uuid.UUID
    position: int
    total: int
    subject: str
    skill: str
    prompt: str
    options: list[str]
    difficulty: int
    source_label: str


class NextQuestionResponse(BaseModel):
    session: SessionResponse
    question: QuestionResponse | None


class AnswerRequest(BaseModel):
    question_id: uuid.UUID
    selected_index: int = Field(ge=0, le=3)


class AnswerResponse(BaseModel):
    correct: bool
    correct_index: int
    feedback: str
    explanation: str
    source_label: str
    mastery_before: int | None
    mastery_after: int
    session_complete: bool
    next_action: str


class TutorHelpRequest(BaseModel):
    learner_id: uuid.UUID
    question_id: uuid.UUID
    message: str = Field(min_length=1, max_length=1_000)


class TutorHelpResponse(BaseModel):
    response: str
    level: Literal[1, 2]
    used_ai: bool
