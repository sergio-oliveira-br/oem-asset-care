# alert-engine/main.py

import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from core.exceptions import AlertEngineException, custom_exception_handler
from services.redis_consumer import redis_consumer

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