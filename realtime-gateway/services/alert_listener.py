import asyncio
import json
import os
import redis.asyncio as aioredis
from services.manager import manager

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

class AlertListener:
    """Escuta os eventos do Redis Pub/Sub e transmite para as conexões WebSocket."""

    async def listen_alerts(self):
        redis_uri = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"
        print(f"[REALTIME GATEWAY] Conectando ao Redis em {redis_uri}...", flush=True)

        while True:
            try:
                client = aioredis.from_url(redis_uri, decode_responses=True)
                pubsub = client.pubsub()

                await pubsub.psubscribe("alerts:*")
                print("[REALTIME GATEWAY] Inscreveu no 'alerts:*'. Aguardando mensagens...", flush=True)

                async for message in pubsub.listen():
                    # Ignora mensagens de confirmação de inscrição
                    if message and message.get("type") == "pmessage":
                        channel = message.get("channel", "")
                        data_str = message.get("data", "")

                        print(f"[PUBSUB RECEBIDO] Canal: {channel} | Dados: {data_str}", flush=True)

                        tenant_id = channel.split(":")[-1] if ":" in channel else None

                        if tenant_id and data_str:
                            try:
                                alert_payload = json.loads(data_str)
                                print(f"[GATEWAY] Repassando para o manager do tenant '{tenant_id}'...", flush=True)
                                await manager.broadcast_to_tenant(tenant_id, alert_payload)
                            except json.JSONDecodeError:
                                print(f"[ERRO PUBSUB] Formato JSON inválido no canal '{channel}'", flush=True)

            except asyncio.CancelledError:
                print("[REALTIME GATEWAY] Task de escuta do Redis encerrada.", flush=True)
                break
            except Exception as e:
                print(f"[ERRO PUBSUB] Falha na conexão com o Redis: {e}. Reconectando em 3s...", flush=True)
                await asyncio.sleep(3)

alert_listener = AlertListener()