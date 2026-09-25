from pydantic import BaseModel


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str


class QuizRequest(BaseModel):
    number: int = 10


class QuizResponse(BaseModel):
    questions: list[str]


class DocumentResponse(BaseModel):
    message: str
    chunks: int