# alert-engine/services/rule_evaluator.py

from services.rules_cache import rules_cache
from services.alert_publisher import alert_publisher

class RuleEvaluator:
    """Responsável exclusivo pela lógica de comparação e detecção de anomalias."""

    def evaluate(self, telemetry: dict) -> None:
        try:
            tenant_id = telemetry.get("tenant_id")
            machine_id = telemetry.get("machine_id")
            metrics = telemetry.get("metrics", {})

            if not tenant_id or not machine_id:
                print("[RULE_EVALUATOR] Telemetria descartada: tenant_id ou machine_id ausentes.")
                return

            temp_atual = metrics.get("temperature", 0.0)
            vib_atual = metrics.get("vibration", 0.0)

            # Busca os limites ativos no cache sem sobrecarregar o banco relacional
            rules = rules_cache.get_machine_rules(tenant_id, machine_id)
            max_temp = rules["max_temperature"]
            max_vib = rules["max_vibration"]

            anomalies = []
            if temp_atual > max_temp:
                anomalies.append(f"Temperatura crítica: {temp_atual}°C (Limiar: {max_temp}°C)")
            if vib_atual > max_vib:
                anomalies.append(f"Vibração excessiva: {vib_atual}g (Limiar: {max_vib}g)")

            if anomalies:
                alert_event = {
                    "tenant_id": tenant_id,
                    "machine_id": machine_id,
                    "timestamp": telemetry.get("timestamp"),
                    "severity": "CRITICAL",
                    "anomalies": anomalies,
                    "metrics": metrics
                }
                alert_publisher.trigger_alert(tenant_id, alert_event)

        except Exception as e:
            print(f"[ERRO RULE_EVALUATOR] Falha durante a avaliação da telemetria: {e}")

rule_evaluator = RuleEvaluator()