// frontend/src/components/TelemetryCard.jsx


export default function TelemetryCard({ telemetry }) {
    const data = telemetry || {
        machine_id: 'MACK-01',
        timestamp: '2026-09-27T12:00:00Z',
        metrics: {
            temperature: 62.4,
            vibration: 0.038,
            running_hours: 1250,
        },
        limits: {
            max_temperature: 75.0,
            max_vibration: 0.050,
        },
    };

    const isTempCritical = data.metrics.temperature > data.limits.max_temperature;
    const isVibCritical = data.metrics.vibration > data.limits.max_vibration;

    return (
        <div style={styles.card}>
            <div style={styles.cardHeader}>
                <span style={styles.machineId}>{data.machine_id}</span>
                <span style={styles.timestamp}>
          {new Date(data.timestamp).toLocaleTimeString()}
        </span>
            </div>

            <div style={styles.grid}>
                {/* Temperatura */}
                <div style={isTempCritical ? styles.metricBoxError : styles.metricBox}>
                    <span style={styles.label}>TEMPERATURA</span>
                    <div style={isTempCritical ? styles.valueError : styles.value}>
                        {data.metrics.temperature.toFixed(1)}
                        <span style={styles.unit}>°C</span>
                    </div>
                    <span style={styles.limit}>Limiar: {data.limits.max_temperature}°C</span>
                </div>

                {/* Vibração */}
                <div style={isVibCritical ? styles.metricBoxError : styles.metricBox}>
                    <span style={styles.label}>VIBRAÇÃO</span>
                    <div style={isVibCritical ? styles.valueError : styles.value}>
                        {data.metrics.vibration.toFixed(3)}
                        <span style={styles.unit}>g</span>
                    </div>
                    <span style={styles.limit}>Limiar: {data.limits.max_vibration}g</span>
                </div>

                {/* Horas de Operação */}
                <div style={styles.metricBox}>
                    <span style={styles.label}>HORAS OPERACIONAIS</span>
                    <div style={styles.value}>
                        {data.metrics.running_hours}
                        <span style={styles.unit}>h</span>
                    </div>
                    <span style={styles.limit}>Status: Normal</span>
                </div>
            </div>
        </div>
    );
}

const styles = {
    card: {
        border: '1px solid #27272a',
        borderRadius: '6px',
        padding: '20px',
        backgroundColor: '#09090b',
        marginBottom: '24px',
    },
    cardHeader: {
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: '20px',
    },
    machineId: {
        fontSize: '14px',
        fontWeight: '600',
        color: '#f4f4f5',
        letterSpacing: '0.5px',
    },
    timestamp: {
        fontSize: '12px',
        color: '#52525b',
    },
    grid: {
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))',
        gap: '12px',
    },
    metricBox: {
        border: '1px solid #18181b',
        backgroundColor: '#121215',
        padding: '16px',
        borderRadius: '4px',
    },
    metricBoxError: {
        border: '1px solid #7f1d1d',
        backgroundColor: '#180707',
        padding: '16px',
        borderRadius: '4px',
    },
    label: {
        display: 'block',
        fontSize: '10px',
        fontWeight: '600',
        color: '#71717a',
        letterSpacing: '0.8px',
        marginBottom: '8px',
    },
    value: {
        fontSize: '28px',
        fontWeight: '500',
        color: '#f4f4f5',
        lineHeight: '1',
    },
    valueError: {
        fontSize: '28px',
        fontWeight: '600',
        color: '#ef4444',
        lineHeight: '1',
    },
    unit: {
        fontSize: '13px',
        color: '#71717a',
        marginLeft: '4px',
        fontWeight: '400',
    },
    limit: {
        display: 'block',
        fontSize: '11px',
        color: '#52525b',
        marginTop: '10px',
    },
};