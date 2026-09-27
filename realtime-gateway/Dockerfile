# realtime-gateway/Dockerfile

FROM python:3.11-slim

WORKDIR /app

# Copia e instala as dependências aproveitando o cache de camadas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código-fonte (core, services, main.py)
COPY . .

EXPOSE 8003

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8003"]