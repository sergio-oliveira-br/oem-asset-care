import json
import redis
from django.conf import settings

class SyncPublisher:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=0,
            decode_responses=True
        )

    def publish_machine_created(self, machine_data):
        payload = json.dumps(machine_data)
        self.redis_client.publish('events:machine_created', payload)

    def publish_threshold_updated(self, tenant_id, machine_id, max_temp, max_vib):
        rule_key = f"rules:{tenant_id}:{machine_id}"

        # Salva em Hash Redis para acesso instantâneo do Alert Engine
        self.redis_client.hset(rule_key, mapping={
            "max_temperature": str(max_temp),
            "max_vibration": str(max_vib)
        })

        payload = json.dumps({
            "tenant_id": tenant_id,
            "machine_id": machine_id,
            "max_temperature": max_temp,
            "max_vibration": max_vib
        })
        self.redis_client.publish('events:threshold_updated', payload)

sync_publisher = SyncPublisher()