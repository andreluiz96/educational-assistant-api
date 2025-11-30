# ============================
# Stage 1 - Build / Dependencies
# ============================
FROM python:3.12-slim AS builder

# Evitar prompts interativos
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Copia apenas o requirements primeiro (melhora cache de build)
COPY requirements.txt .

# Instala dependências em uma pasta isolada (/install)
RUN pip install --prefix=/install -r requirements.txt


# ============================
# Stage 2 - Runtime
# ============================
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copia as dependências do stage builder
COPY --from=builder /install /usr/local

# Copia o código da aplicação
COPY app ./app
COPY requirements.txt .

# Expor a porta usada pelo Uvicorn
EXPOSE 8000

# Comando padrão ao subir o container
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
