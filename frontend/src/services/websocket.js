// frontend/src/services/websocket.js

/**
 * Gerenciador de Conexão WebSocket
 * @param {string} url - Endereço do gateway (ex: ws://localhost:8003/ws)
 * @param {Object} handlers - Callbacks de mensagem e status
 */
export function connectWebSocket(url, { onMessage, onStatusChange }) {
    let socket = new WebSocket(url);

    socket.onopen = () => {
        if (onStatusChange) onStatusChange(true);
    };

    socket.onmessage = (event) => {
        try {
            const payload = JSON.parse(event.data);
            if (onMessage) onMessage(payload);
        } catch (err) {
            console.error('[WS Error] Falha ao processar payload JSON:', err);
        }
    };

    socket.onerror = (error) => {
        console.error('[WS Error]', error);
    };

    socket.onclose = () => {
        if (onStatusChange) onStatusChange(false);
    };

    // Retorna função de teardown/cleanup
    return () => {
        if (socket && socket.readyState === WebSocket.OPEN) {
            socket.close();
        }
    };
}