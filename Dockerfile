# ============================
# Stage 1 - Dependências
# ============================
FROM python:3.12-slim AS builder

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Copia o requirements da raiz do projeto
COPY requirements.txt .

# Instala dependências em uma pasta isolada (/install)
RUN pip install --prefix=/install -r requirements.txt


# ============================
# Stage 2 - Runtime
# ============================
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copia as dependências instaladas no stage builder
COPY --from=builder /install /usr/local

# Copia o código da aplicação (FastAPI)
# (app/main.py está dentro de backend/app)
COPY backend/app ./app

# Porta usada pelo Uvicorn
EXPOSE 8000

# Comando padrão ao subir o container
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
