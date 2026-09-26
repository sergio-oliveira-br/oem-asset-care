# core-api/alert_configs/views.py

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, serializers
from .models import AlertConfig
from core.sync_publisher import sync_publisher

class AlertConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertConfig
        fields = ['machine', 'max_temperature', 'max_vibration', 'updated_at']

@api_view(['PUT', 'PATCH'])
def update_threshold(request, machine_id):
    try:
        config = AlertConfig.objects.get(machine_id=machine_id)
    except AlertConfig.DoesNotExist:
        return Response({"detail": "Configuração de alerta não encontrada para esta máquina."}, status=status.HTTP_404_NOT_FOUND)

    serializer = AlertConfigSerializer(config, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()

        # Publica a atualização de limiar no Redis
        sync_publisher.publish_threshold_updated(
            config.machine.tenant.tenant_id,
            config.machine.machine_id,
            config.max_temperature,
            config.max_vibration
        )

        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
