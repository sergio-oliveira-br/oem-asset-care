# iot-simulator/main.py

import paho.mqtt.client as mqtt
import os
import json
import random
import time
from datetime import datetime, timezone


MQTT_HOST = os.getenv("MQTT_BROKER_HOST", "mosquitto")
MQTT_PORT = int(os.getenv("MQTT_BROKER_PORT", 1883))


# Configurações de Conexão com o Broker MQTT
# BROKER_HOST = "localhost"
# BROKER_PORT = 1883
TOPIC = "telemetry/v1/data"

# Identificadores de Contexto Multi-tenant e Máquina
TENANT_ID = "tenant-01"
MACHINE_ID = "MACK-01"


def create_mqtt_client():
    """Cria e conecta o cliente MQTT ao broker Mosquitto."""
    client = mqtt.Client(client_id=f"sim_{MACHINE_ID}")
    try:
        client.connect(MQTT_HOST, MQTT_PORT, keepalive=60)
        print(f"[MQTT] Conectado ao Broker {MQTT_HOST}:{MQTT_PORT}")
        return client
    except Exception as e:
        print(f"[ERRO] Falha ao conectar no Broker MQTT: {e}")
        return None


def generate_telemetry_payload(inject_anomaly: bool = False):
    """
    Gera leituras verossímeis de sensores da máquina.
    Se inject_anomaly=True, força um pico térmico no equipamento.
    """
    # Operação Normal: Temperatura entre 55°C e 68°C
    base_temp = random.uniform(55.0, 68.0)

    # Injeção de Falha: Temperatura salta para 82°C - 95°C (Superaquecimento)
    if inject_anomaly:
        base_temp = random.uniform(82.0, 95.0)
        print("[!] [INJEÇÃO DE FALHA ATIVA] Gerando temperatura crítica de anomalia!")

    payload = {
        "tenant_id": TENANT_ID,
        "machine_id": MACHINE_ID,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "metrics": {
            "temperature": round(base_temp, 2),
            "vibration": round(random.uniform(0.01, 0.08), 3),
            "running_hours": 1250
        }
    }
    return payload


def main():
    client = create_mqtt_client()
    if not client:
        return

    client.loop_start()
    print(f"[SIMULADOR] Enviando telemetrias para a máquina {MACHINE_ID}...")
    print("Pressione CTRL+C para encerrar.\n")

    counter = 0
    try:
        while True:
            counter += 1
            # A cada 10 envios, induz uma anomalia para testar a detecção
            anomaly_flag = True if counter % 10 == 0 else False

            data = generate_telemetry_payload(inject_anomaly=anomaly_flag)
            json_payload = json.dumps(data)

            # Publica a mensagem no tópico MQTT
            result = client.publish(TOPIC, json_payload)
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                print(f"[{data['timestamp']}] Enviado: Temp = {data['metrics']['temperature']}°C | Vib = {data['metrics']['vibration']}")
            else:
                print("[ERRO] Falha ao publicar mensagem no tópico MQTT.")

            time.sleep(2)  # Intervalo de 2 segundos entre leituras

    except KeyboardInterrupt:
        print("\n[SIMULADOR] Encerrando simulador...")
    finally:
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    main()