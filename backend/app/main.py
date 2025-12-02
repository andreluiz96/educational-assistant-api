# backend/app/main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from groq import Groq
import os

# ========== Config ==========
load_dotenv()  # carrega variáveis do .env (útil em desenvolvimento)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    # Em produção (ECS), essa variável vem do ambiente da task
    # Em dev, vem do arquivo .env
    raise RuntimeError("GROQ_API_KEY não está configurada.")

client = Groq(api_key=GROQ_API_KEY)
MODEL_NAME = "llama-3.1-8b-instant"  # modelo leve para POC

app = FastAPI(
    title="Educational Assistant API",
    version="2.0.0",
    description="Backend de prova de conceito para assistente educacional usando Groq LLM.",
)

# ========== Models ==========

class QuestionRequest(BaseModel):
    student_id: str
    question: str


class AnswerResponse(BaseModel):
    student_id: str
    question: str
    answer: str


class HealthResponse(BaseModel):
    status: str
    version: str | None = None


# ========== Rotas ==========

@app.get("/health", response_model=HealthResponse)
def health_check():
    return HealthResponse(status="ok", version="2")


@app.post("/ask", response_model=AnswerResponse)
def ask_question(payload: QuestionRequest):
    """
    Recebe uma pergunta do aluno e retorna uma resposta explicativa do LLM.
    """
    system_prompt = (
        "Você é um assistente educacional paciente e didático para estudantes de "
        "nível introdutório de computação. Explique os conceitos em linguagem simples, "
        "com exemplos práticos do dia a dia. Responda sempre em português do Brasil."
    )

    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": (
                        f"ID do aluno: {payload.student_id}\n\n"
                        f"Pergunta do aluno: {payload.question}"
                    ),
                },
            ],
            temperature=0.4,
            max_tokens=600,
        )

        answer_text = completion.choices[0].message.content.strip()

        return AnswerResponse(
            student_id=payload.student_id,
            question=payload.question,
            answer=answer_text,
        )

    except Exception as e:
        # Aqui você ainda consegue ver o erro real nos logs
        print("ERRO AO CHAMAR LLM:", repr(e))
        raise HTTPException(
            status_code=500, detail="Erro ao processar pergunta."
        )
