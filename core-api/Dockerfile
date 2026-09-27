# core-api/Dockerfile

FROM python:3.11-slim

WORKDIR /app

# Instala dependências do sistema necessárias para o psycopg2 e compilação
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Executa as migrações automáticas e inicia o servidor HTTP do Django
CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py runserver 0.0.0.0:8000"]