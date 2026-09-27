# alert-engine/services/alert_publisher.py

import json
from services.rules_cache import redis_client

class AlertPublisher:
    """Responsável exclusivo por formatar e emitir alertas para o Pub/Sub."""

    def trigger_alert(self, tenant_id: str, alert_data: dict) -> None:
        try:
            channel = f"alerts:{tenant_id}"
            payload = json.dumps(alert_data)
            redis_client.publish(channel, payload)
            print(f"[!] [ALERTA DISPARADO] Canal '{channel}': {payload}")
        except Exception as e:
            print(f"[ERRO ALERT_PUBLISHER] Falha ao emitir alerta no Redis PubSub: {e}")

alert_publisher = AlertPublisher()