from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class QuestionRequest(BaseModel):
    student_id: str
    question: str

class AnswerResponse(BaseModel):
    student_id: str
    question: str
    answer: str

class HealthResponse(BaseModel):
    status: str
    version: str

# ---- Rotas ----

@app.get("/health", response_model=HealthResponse)
def health():
    return HealthResponse(status="ok", version="2")



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
