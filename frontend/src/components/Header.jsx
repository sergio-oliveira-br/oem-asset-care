// frontend/src/components/Header.jsx


export default function Header({ isConnected }) {
    return (
        <header style={styles.header}>
            <div style={styles.brand}>
                <span style={styles.title}>OEM ASSET CARE</span>
                <span style={styles.separator}>/</span>
                <span style={styles.tenant}>tenant-01</span>
            </div>

            <div style={styles.status}>
                <span style={isConnected ? styles.dotConnected : styles.dotDisconnected}></span>
                <span>{isConnected ? 'ONLINE' : 'DESCONECTADO'}</span>
            </div>
        </header>
    );
}

const styles = {
    header: {
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        paddingBottom: '16px',
        borderBottom: '1px solid #27272a',
        marginBottom: '32px',
    },
    brand: { display: 'flex', alignItems: 'center', gap: '12px' },
    title: { fontSize: '13px', fontWeight: '700', letterSpacing: '1px', color: '#f4f4f5' },
    separator: { color: '#3f3f46' },
    tenant: { fontSize: '13px', color: '#71717a' },
    status: {
        display: 'flex',
        alignItems: 'center',
        gap: '8px',
        fontSize: '11px',
        letterSpacing: '0.5px',
        color: '#71717a',
    },
    dotConnected: {
        width: '6px',
        height: '6px',
        borderRadius: '50%',
        backgroundColor: '#22c55e',
    },
    dotDisconnected: {
        width: '6px',
        height: '6px',
        borderRadius: '50%',
        backgroundColor: '#ef4444',
    },
};