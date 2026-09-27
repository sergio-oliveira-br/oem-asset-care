# alert-engine/services/redis_consumer.py

import json
import asyncio
import redis
import os
from services.rule_evaluator import rule_evaluator

STREAM_KEY = "telemetry:stream"
CONSUMER_GROUP = "alert_engine_group"
CONSUMER_NAME = "alert_engine_worker_1"

class RedisConsumer:
    """Responsável exclusivo pela leitura contínua de eventos do Redis Streams."""

    def __init__(self):
        self.redis_client = redis.Redis(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=int(os.getenv("REDIS_PORT", 6379)),
            db=0,
            decode_responses=True
        )
        self._init_consumer_group()

    def _init_consumer_group(self):
        try:
            self.redis_client.xgroup_create(STREAM_KEY, CONSUMER_GROUP, id="0", mkstream=True)
        except redis.exceptions.ResponseError as e:
            if "BUSYGROUP" not in str(e):
                print(f"[REDIS_CONSUMER] Aviso ao inicializar Consumer Group: {e}")

    async def read_telemetry_stream(self) -> None:
        print(f"[REDIS_CONSUMER] Escutando o fluxo Redis Stream '{STREAM_KEY}'...")
        while True:
            try:
                # Lê mensagens não processadas usando XREADGROUP
                entries = self.redis_client.xreadgroup(
                    groupname=CONSUMER_GROUP,
                    consumername=CONSUMER_NAME,
                    streams={STREAM_KEY: ">"},
                    count=10,
                    block=2000
                )

                if entries:
                    for stream_name, messages in entries:
                        for msg_id, msg_data in messages:
                            try:
                                payload_str = msg_data.get("payload")
                                if payload_str:
                                    telemetry = json.loads(payload_str)
                                    rule_evaluator.evaluate(telemetry)

                                # Confirma o processamento da mensagem no Redis Stream
                                self.redis_client.xack(STREAM_KEY, CONSUMER_GROUP, msg_id)
                            except Exception as parse_error:
                                print(f"[REDIS_CONSUMER] Erro no parse/ACK da mensagem {msg_id}: {parse_error}")

            except Exception as conn_error:
                print(f"[REDIS_CONSUMER] Conexão com Redis interrompida. Reagendando em 2s: {conn_error}")
                await asyncio.sleep(2)

            await asyncio.sleep(0.01)

redis_consumer = RedisConsumer()