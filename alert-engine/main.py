# alert-engine/main.py

import os
import redis
import asyncio
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from core.exceptions import AlertEngineException, custom_exception_handler
from services.redis_consumer import redis_consumer


REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicia o leitor assíncrono do Redis Stream no startup da aplicação
    asyncio.create_task(redis_consumer.read_telemetry_stream())
    yield

app = FastAPI(
    title="OEM Asset Care - Alert & Stream Engine",
    version="1.0.0",
    lifespan=lifespan
)

app.add_exception_handler(AlertEngineException, custom_exception_handler)

@app.get("/health")
def health_check():
    return {"status": "UP", "service": "alert-engine"}

# Mantém o servidor rodando e escutando requisições ao executar `python main.py`
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)