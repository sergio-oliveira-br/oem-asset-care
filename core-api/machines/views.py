# core-api/machines/views.py

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, serializers
from .models import Machine
from alert_configs.models import AlertConfig
from core.sync_publisher import sync_publisher

class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = ['machine_id', 'tenant', 'name', 'created_at']

@api_view(['POST'])
def register_machine(request):
    serializer = MachineSerializer(data=request.data)
    if serializer.is_valid():
        machine = serializer.save()

        # Cria configuração padrão de alerta ao registrar máquina
        alert_config, _ = AlertConfig.objects.get_or_create(machine=machine)

        # Notifica o evento
        payload = {
            "tenant_id": machine.tenant.tenant_id,
            "machine_id": machine.machine_id,
            "name": machine.name
        }
        sync_publisher.publish_machine_created(payload)
        sync_publisher.publish_threshold_updated(
            machine.tenant.tenant_id,
            machine.machine_id,
            alert_config.max_temperature,
            alert_config.max_vibration
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
