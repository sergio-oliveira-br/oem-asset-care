# realtime-gateway/services/manager.py

import json
from typing import Dict, List
from fastapi import WebSocket

class ConnectionManager:
    """Gerencia conexões WebSocket ativas agrupadas por tenant_id."""

    def __init__(self):
        # Mapeamento: tenant_id -> lista de conexões WebSocket ativas
        self.active_sessions: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket):
        await websocket.accept()

    def register_session(self, tenant_id: str, websocket: WebSocket):
        if tenant_id not in self.active_sessions:
            self.active_sessions[tenant_id] = []
        self.active_sessions[tenant_id].append(websocket)
        print(f"[Conectado] [WEBSOCKET] Nova conexão registrada para tenant '{tenant_id}'. Total ativas: {len(self.active_sessions[tenant_id])}")

    def handle_disconnect(self, tenant_id: str, websocket: WebSocket):
        if tenant_id in self.active_sessions:
            if websocket in self.active_sessions[tenant_id]:
                self.active_sessions[tenant_id].remove(websocket)
                print(f"[Desconectado] [WEBSOCKET] Conexão encerrada para tenant '{tenant_id}'. Restantes: {len(self.active_sessions[tenant_id])}")
            if not self.active_sessions[tenant_id]:
                del self.active_sessions[tenant_id]

    async def broadcast_to_tenant(self, tenant_id: str, message: dict):
        """Transmite o alerta apenas para os sockets do tenant afetado."""
        if tenant_id in self.active_sessions:
            payload = json.dumps(message)
            disconnected_sockets = []

            for connection in self.active_sessions[tenant_id]:
                try:
                    await connection.send_text(payload)
                except Exception as e:
                    print(f"[WEBSOCKET] Erro ao enviar mensagem, agendando remoção: {e}")
                    disconnected_sockets.append(connection)

            # Limpa conexões mortas detectadas durante a transmissão
            for dead_socket in disconnected_sockets:
                self.handle_disconnect(tenant_id, dead_socket)

manager = ConnectionManager()