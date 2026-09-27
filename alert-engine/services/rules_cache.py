# alert-engine/services/rules_cache.py

import os
import redis

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    db=0,
    decode_responses=True
)

class RulesCache:
    """Responsável exclusivo pela busca de regras e limiares no Redis."""

    def get_machine_rules(self, tenant_id: str, machine_id: str) -> dict:
        try:
            rule_key = f"rules:{tenant_id}:{machine_id}"
            rules = redis_client.hgetall(rule_key)
            if not rules:
                # Fallback seguro caso a máquina ainda não tenha regras cadastradas
                return {"max_temperature": 75.0, "max_vibration": 0.05}

            return {
                "max_temperature": float(rules.get("max_temperature", 75.0)),
                "max_vibration": float(rules.get("max_vibration", 0.05))
            }
        except Exception as e:
            print(f"[ERRO RULES_CACHE] Falha ao consultar Redis para {tenant_id}/{machine_id}: {e}")
            return {"max_temperature": 75.0, "max_vibration": 0.05}

rules_cache = RulesCache()