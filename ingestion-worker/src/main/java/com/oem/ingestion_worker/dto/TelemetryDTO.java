// src/main/java/com/oem/ingestion_worker/dto/TelemetryDTO.java

package com.oem.ingestion_worker.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

@Data
public class TelemetryDTO {

    @JsonProperty("tenant_id")
    private String tenantId;

    @JsonProperty("machine_id")
    private String machineId;

    private String timestamp;

    private Metrics metrics;

    @Data
    public static class Metrics {
        private Double temperature;
        private Double vibration;

        @JsonProperty("running_hours")
        private Integer runningHours;
    }
}