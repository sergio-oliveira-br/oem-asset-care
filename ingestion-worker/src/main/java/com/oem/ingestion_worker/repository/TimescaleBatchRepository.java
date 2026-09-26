// src/main/java/com/oem/ingestion_worker/repository/TimescaleBatchRepository.java

package com.oem.ingestion_worker.repository;

import com.oem.ingestion_worker.dto.TelemetryDTO;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Repository;

import java.time.OffsetDateTime;
import java.util.List;

@Slf4j
@Repository
@RequiredArgsConstructor
public class TimescaleBatchRepository {

    private final JdbcTemplate jdbcTemplate;

    public void saveBatch(List<TelemetryDTO> telemetryList) {
        String sql = """
            INSERT INTO telemetry_data (timestamp, tenant_id, machine_id, temperature, vibration, running_hours)
            VALUES (?, ?, ?, ?, ?, ?)
        """;

        jdbcTemplate.batchUpdate(sql, telemetryList, telemetryList.size(), (ps, dto) -> {
            ps.setObject(1, OffsetDateTime.parse(dto.getTimestamp()));
            ps.setString(2, dto.getTenantId());
            ps.setString(3, dto.getMachineId());
            ps.setDouble(4, dto.getMetrics().getTemperature());
            ps.setDouble(5, dto.getMetrics().getVibration());
            ps.setInt(6, dto.getMetrics().getRunningHours());
        });

        log.info("[TIMESCALEDB] Lote de {} registros persistido com sucesso!", telemetryList.size());
    }
}