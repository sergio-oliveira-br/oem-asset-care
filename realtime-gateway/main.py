# realtime-gateway/main.py

import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query
from core.jwt_validator import jwt_validator
from services.manager import manager
from services.alert_listener import alert_listener

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicia a escuta de alertas no Redis Pub/Sub em segundo plano
    listener_task = asyncio.create_task(alert_listener.listen_alerts())
    yield
    listener_task.cancel()

app = FastAPI(
    title="OEM Asset Care - Realtime Gateway",
    version="1.0.0",
    lifespan=lifespan
)

@app.websocket("/ws/alerts")
async def websocket_alerts_endpoint(
        websocket: WebSocket,
        token: str = Query(..., description="Token JWT de autenticação contendo o tenant_id")
):
    # 1. Conecta o socket
    await manager.connect(websocket)

    tenant_id = None
    try:
        # 2. Decodifica o token JWT e valida a sessão
        payload = jwt_validator.decode_token(token)
        tenant_id = payload.get("tenant_id")

        # 3. Registra a conexão na sala do tenant
        manager.register_session(tenant_id, websocket)

        # Envia mensagem de boas-vindas / handshake concluído
        await websocket.send_json({
            "event": "CONNECTED",
            "message": f"Conexao em tempo real estabelecida para o tenant '{tenant_id}'."
        })

        # Mantém a conexão aberta aguardando mensagens ou desconexão do cliente
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        if tenant_id:
            manager.handle_disconnect(tenant_id, websocket)
    except Exception as e:
        print(f"[WEBSOCKET ERRO] Falha no ciclo de vida do socket: {e}")
        if tenant_id:
            manager.handle_disconnect(tenant_id, websocket)
        await websocket.close()

@app.get("/health")
def health_check():
    return {"status": "UP", "service": "realtime-gateway"}