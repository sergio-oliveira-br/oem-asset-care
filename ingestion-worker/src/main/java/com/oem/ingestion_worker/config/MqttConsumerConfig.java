package com.oem.ingestion_worker.config;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.oem.ingestion_worker.dto.TelemetryDTO;
import com.oem.ingestion_worker.repository.TimescaleBatchRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.integration.annotation.ServiceActivator;
import org.springframework.integration.channel.DirectChannel;
import org.springframework.integration.core.MessageProducer;
import org.springframework.integration.mqtt.core.DefaultMqttPahoClientFactory;
import org.springframework.integration.mqtt.core.MqttPahoClientFactory;
import org.springframework.integration.mqtt.inbound.MqttPahoMessageDrivenChannelAdapter;
import org.springframework.integration.mqtt.support.DefaultPahoMessageConverter;
import org.springframework.messaging.MessageChannel;
import org.springframework.messaging.MessageHandler;


import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

@Slf4j
@Configuration
@RequiredArgsConstructor

public class MqttConsumerConfig {

    @Value("${mqtt.broker-url}")
    private String brokerUrl;

    @Value("${mqtt.client-id}")
    private String clientId;

    @Value("${mqtt.topic}")
    private String topic;

    @Value("${mqtt.batch-size}")
    private int batchSize;

    private final TimescaleBatchRepository batchRepository;
    private final ObjectMapper objectMapper = new ObjectMapper();
    private final List<TelemetryDTO> buffer = Collections.synchronizedList(new ArrayList<>());

    @Bean
    public MqttPahoClientFactory mqttClientFactory() {
        DefaultMqttPahoClientFactory factory = new DefaultMqttPahoClientFactory();
        MqttConnectOptions options = new MqttConnectOptions();
        options.setServerURIs(new String[]{brokerUrl});
        options.setCleanSession(true);
        factory.setConnectionOptions(options);
        return factory;
    }

    @Bean
    public MessageChannel mqttInputChannel() {
        return new DirectChannel();
    }

    @Bean
    public MessageProducer inbound() {
        MqttPahoMessageDrivenChannelAdapter adapter =
                new MqttPahoMessageDrivenChannelAdapter(clientId, mqttClientFactory(), topic);
        adapter.setCompletionTimeout(5000);
        adapter.setConverter(new DefaultPahoMessageConverter());
        adapter.setQos(1);
        adapter.setOutputChannel(mqttInputChannel());
        return adapter;
    }

    @Bean
    @ServiceActivator(inputChannel = "mqttInputChannel")
    public MessageHandler handler() {
        return message -> {
            try {
                String payload = (String) message.getPayload();
                TelemetryDTO dto = objectMapper.readValue(payload, TelemetryDTO.class);

                buffer.add(dto);

                // Executa flush quando o buffer atinge o tamanho configurado
                if (buffer.size() >= batchSize) {
                    synchronized (buffer) {
                        batchRepository.saveBatch(new ArrayList<>(buffer));
                        buffer.clear();
                    }
                }
            } catch (Exception e) {
                log.error("[ERRO INGESTÃO] Falha ao processar mensagem MQTT: {}", e.getMessage());
            }
        };
    }
}