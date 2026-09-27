# OEM Asset Care

Plataforma unificada de telemetria e monitoramento de ativos industriais em tempo real. O sistema simula a coleta de dados de dispositivos IoT, processa métricas operacionais por meio de uma arquitetura baseada em eventos e exibe o status de saúde e alertas na interface do usuário.

Este projeto foi desenvolvido como um exercício prático de engenharia de software para validar a integração de microsserviços poliglotas, orquestração de contêineres e comunicação em tempo real.

---

## Arquitetura e Fluxo de Dados

A solução opera através de um pipeline desacoplado onde cada componente possui uma responsabilidade bem definida:

1. Simulação: O serviço de simulação IoT gera métricas operacionais fictícias de máquinas e publica mensagens via protocolo MQTT.
2. Ingestão: O broker MQTT (Mosquitto) recebe os dados e o serviço de ingestão em Java (Spring Boot) consome os pacotes, persistindo métricas temporais no TimescaleDB e publicando eventos no Redis Streams.
3. Processamento de Alertas: O motor de alertas em Python consome os eventos do Redis, avalia anomalias com base em regras operacionais e gera alertas.
4. Distribuição em Tempo Real: O gateway em FastAPI consome as notificações do Redis e as transmite para os clientes via WebSocket.
5. Visualização: A interface em React (servida via Nginx) exibe o painel de telemetria e atualiza o feed de alertas instantaneamente.

---

## Tecnologias Utilizadas

### Frontend
- React com Vite
- Nginx como proxy reverso e servidor estático

### Backend e Serviços
- Django REST Framework (Core API e regras de negócio)
- Spring Boot / Java 21 (Ingestão de alta performance)
- FastAPI / Python 3.12 (Realtime Gateway WebSocket e Engine de Alertas)
- Python Script (Simulador de telemetria IoT)

### Banco de Dados e Mensageria
- TimescaleDB (PostgreSQL otimizado para séries temporais)
- Redis / Redis Streams (Cache e barramento de eventos pub/sub)
- Eclipse Mosquitto (Broker MQTT)

### Infraestrutura
- Docker e Docker Compose (Orquestração local com healthchecks)

---

## Estrutura dos Serviços

| Serviço | Contêiner | Porta Interna | Porta Host | Função |
|---|---|---|---|---|
| Frontend | oem_frontend | 80 | 80 | Interface do usuário e roteamento de WebSocket |
| Core API | oem_core_business | 8000 | 8000 | Gestão de ativos e API administrativa (Django) |
| Realtime Gateway | oem_realtime_gateway | 8003 | 8003 | Servidor WebSocket para dados ao vivo |
| Ingestion Worker | oem_ingestion_worker | 8080 | Interna | Consumidor MQTT e gravador de dados |
| Alert Engine | oem_alert_engine | 8001 | Interna | Processador de regras de anomalias |
| IoT Simulator | oem_iot_simulator | - | Interna | Gerador de dados de telemetria |
| Mosquitto | oem_mosquitto | 1883 | 1883 | Broker MQTT |
| TimescaleDB | oem_timescaledb | 5432 | 5433 | Armazenamento de séries temporais |
| Redis | oem_redis | 6379 | 6379 | Cache e pub/sub de eventos |

---

## Como Executar a Aplicação

### Pré-requisitos
- Docker Engine 20.10 ou superior
- Docker Compose v2 ou superior

### Passos para Inicialização

1. Clone este repositório para o seu ambiente local:
   git clone <url-do-repositorio>
   cd oem-asset-care

2. Execute o comando para compilar as imagens e iniciar toda a stack de contêineres:
   docker compose up -d --build

3. Acompanhe a inicialização dos serviços e migrações:
   docker compose logs -f

---

## Pontos de Acesso

Com a stack em execução, as seguintes URLs ficam disponíveis localmente:

- Painel Principal (Frontend): http://localhost
- API Core (Django Admin): http://localhost:8000/admin/
- Documentação Realtime Gateway (FastAPI): http://localhost:8003/docs
