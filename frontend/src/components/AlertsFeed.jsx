// frontend/src/components/AlertsFeed.jsx

export default function AlertsFeed({ alerts }) {
    // Lista fallback estática para validação visual
    const alertList = alerts || [
        {
            id: 'alt-003',
            timestamp: '2026-09-27T12:02:15Z',
            machine_id: 'MACK-01',
            type: 'VIBRAÇÃO ELEVADA',
            severity: 'CRITICAL',
            message: 'Medido: 0.054g (Limiar: 0.050g)',
        },
        {
            id: 'alt-002',
            timestamp: '2026-09-27T11:45:00Z',
            machine_id: 'MACK-01',
            type: 'TEMPERATURA ELEVADA',
            severity: 'CRITICAL',
            message: 'Medido: 76.2°C (Limiar: 75.0°C)',
        },
        {
            id: 'alt-001',
            timestamp: '2026-09-27T10:15:30Z',
            machine_id: 'MACK-01',
            type: 'RECONEXÃO WEBSOCKET',
            severity: 'INFO',
            message: 'Sessão restabelecida via Broker Redis',
        },
    ];

    return (
        <div style={styles.container}>
            <div style={styles.header}>
                <span style={styles.title}>LOG DE EVENTOS E ALERTAS</span>
                <span style={styles.count}>{alertList.length} EVENTOS</span>
            </div>

            <div style={styles.list}>
                {alertList.map((alert) => {
                    const isCritical = alert.severity === 'CRITICAL';

                    return (
                        <div
                            key={alert.id}
                            style={isCritical ? styles.rowCritical : styles.rowInfo}
                        >
                            <div style={styles.rowHeader}>
                <span style={styles.time}>
                  {new Date(alert.timestamp).toLocaleTimeString()}
                </span>
                                <span style={styles.machine}>{alert.machine_id}</span>
                                <span style={isCritical ? styles.badgeCritical : styles.badgeInfo}>
                  {alert.severity}
                </span>
                            </div>

                            <div style={styles.rowBody}>
                                <span style={styles.eventType}>{alert.type}</span>
                                <span style={styles.message}>{alert.message}</span>
                            </div>
                        </div>
                    );
                })}
            </div>
        </div>
    );
}

const styles = {
    container: {
        border: '1px solid #27272a',
        borderRadius: '6px',
        backgroundColor: '#09090b',
        padding: '20px',
    },
    header: {
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        paddingBottom: '12px',
        borderBottom: '1px solid #18181b',
        marginBottom: '16px',
    },
    title: {
        fontSize: '11px',
        fontWeight: '700',
        color: '#71717a',
        letterSpacing: '0.8px',
    },
    count: {
        fontSize: '11px',
        color: '#52525b',
    },
    list: {
        display: 'flex',
        flexDirection: 'column',
        gap: '8px',
        maxHeight: '360px',
        overflowY: 'auto',
    },
    rowInfo: {
        border: '1px solid #18181b',
        backgroundColor: '#121215',
        padding: '12px',
        borderRadius: '4px',
    },
    rowCritical: {
        border: '1px solid #7f1d1d',
        backgroundColor: '#180707',
        padding: '12px',
        borderRadius: '4px',
    },
    rowHeader: {
        display: 'flex',
        alignItems: 'center',
        gap: '12px',
        marginBottom: '6px',
    },
    time: {
        fontSize: '11px',
        fontFamily: 'monospace',
        color: '#71717a',
    },
    machine: {
        fontSize: '11px',
        fontWeight: '600',
        color: '#a1a1aa',
    },
    badgeInfo: {
        fontSize: '9px',
        fontWeight: '700',
        color: '#71717a',
        border: '1px solid #27272a',
        padding: '1px 5px',
        borderRadius: '2px',
    },
    badgeCritical: {
        fontSize: '9px',
        fontWeight: '700',
        color: '#ef4444',
        border: '1px solid #7f1d1d',
        padding: '1px 5px',
        borderRadius: '2px',
    },
    rowBody: {
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
    },
    eventType: {
        fontSize: '12px',
        fontWeight: '600',
        color: '#f4f4f5',
    },
    message: {
        fontSize: '12px',
        color: '#a1a1aa',
    },
};