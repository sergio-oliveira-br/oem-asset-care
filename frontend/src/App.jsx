import { useState, useEffect } from 'react';
import Header from './components/Header';
import TelemetryCard from './components/TelemetryCard';
import AlertsFeed from './components/AlertsFeed';
import { connectWebSocket } from './services/websocket';

export default function App() {
  const [isConnected, setIsConnected] = useState(false);

  const [telemetry, setTelemetry] = useState({
    machine_id: 'MACK-01',
    timestamp: new Date().toISOString(),
    metrics: { temperature: 0, vibration: 0, running_hours: 0 },
    limits: { max_temperature: 75.0, max_vibration: 0.050 },
  });

  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    // URL e token reais validados no realtime-gateway
    const WS_URL = 'ws://localhost:8003/ws/alerts?token=test-token-tenant-01';

    const disconnect = connectWebSocket(WS_URL, {
      onStatusChange: (status) => setIsConnected(status),
      onMessage: (payload) => {
        // 1. Atualiza o card de telemetria com as métricas do evento
        if (payload.metrics) {
          setTelemetry({
            machine_id: payload.machine_id,
            timestamp: payload.timestamp,
            metrics: payload.metrics,
            limits: { max_temperature: 75.0, max_vibration: 0.040 },
          });
        }

        // 2. Registra o alerta no feed
        const newAlert = {
          id: `alt-${Date.now()}`,
          timestamp: payload.timestamp,
          machine_id: payload.machine_id,
          type: payload.anomalies?.[0] || 'ANOMALIA DETECTADA',
          severity: payload.severity,
          message: `Temp: ${payload.metrics.temperature}°C | Vib: ${payload.metrics.vibration}g`,
        };

        setAlerts((prev) => [newAlert, ...prev]);
      },
    });

    return () => disconnect();
  }, []);

  return (
      <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
        <Header isConnected={isConnected} />

        <main style={styles.grid}>
          <div>
            <TelemetryCard telemetry={telemetry} />
          </div>
          <div>
            <AlertsFeed alerts={alerts} />
          </div>
        </main>
      </div>
  );
}

const styles = {
  grid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(340px, 1fr))',
    gap: '24px',
  },
};