from fastapi import FastAPI
from pydantic import BaseModel

from typing import List

app = FastAPI(
    title="Educational Assistant API",
    version="1.0.0",
    description="Assistente educacional em arquitetura cloud moderna."
)

# ---- Schemas ----

class QuestionRequest(BaseModel):
    student_id: str
    question: str

class AnswerResponse(BaseModel):
    student_id: str
    question: str
    answer: str

class HealthResponse(BaseModel):
    status: str

# ---- Rotas ----

@app.get("/health", response_model=HealthResponse)
def health_check():
    return HealthResponse(status="ok")

@app.get("/health")
def health():
    return {"status": "ok", "version": "2"}


@app.post("/ask", response_model=AnswerResponse)
def ask_question(payload: QuestionRequest):
    """
    Por enquanto, resposta mockada.
    Depois a gente troca por chamada a um LLM (OpenAI, etc.).
    """
    mock_answer = (
        "Sou um assistente educacional. "
        "Em breve vou responder usando um modelo de IA de verdade. "
        f"Você perguntou: {payload.question}"
    )

    return AnswerResponse(
        student_id=payload.student_id,
        question=payload.question,
        answer=mock_answer
    )
