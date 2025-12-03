# backend/app/main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from groq import Groq
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import os
import json
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

templates = Jinja2Templates(directory="app/templates")

app = FastAPI(
    title="Educational Assistant API",
    version="2.0.0"
)

# Servir arquivos estáticos (se quiser futuramente)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# ========== Config ==========
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

load_dotenv()  # carrega variáveis do .env em dev

raw_key = os.getenv("GROQ_API_KEY")
if not raw_key:
    raise RuntimeError("GROQ_API_KEY não está configurada.")

# Se em algum ambiente vier JSON, trata; se for texto simples, usa direto
try:
    maybe_json = json.loads(raw_key)
    if isinstance(maybe_json, dict) and "GROQ_API_KEY" in maybe_json:
        GROQ_API_KEY = maybe_json["GROQ_API_KEY"]
    else:
        GROQ_API_KEY = raw_key
except json.JSONDecodeError:
    GROQ_API_KEY = raw_key

client = Groq(api_key=GROQ_API_KEY)
MODEL_NAME = "llama-3.1-8b-instant"

app = FastAPI(
    title="Educational Assistant API",
    version="2.0.0",
    description="Backend de prova de conceito para assistente educacional usando Groq LLM.",
)

# montar arquivos estáticos (CSS/JS)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


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

@app.get("/", response_class=HTMLResponse)
def frontend():
    """
    Entrega a página do assistente educacional.
    """
    index_path = STATIC_DIR / "index.html"
    return index_path.read_text(encoding="utf-8")


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
        print("ERRO AO CHAMAR LLM:", repr(e))
        raise HTTPException(
            status_code=500, detail="Erro ao processar pergunta."
        )
