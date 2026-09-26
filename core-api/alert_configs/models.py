# core-api/alert_configs/models.py

from django.db import models
from machines.models import Machine

class AlertConfig(models.Model):
    machine = models.OneToOneField(Machine, on_delete=models.CASCADE, primary_key=True, related_name='alert_config')
    max_temperature = models.FloatField(default=75.0)
    max_vibration = models.FloatField(default=0.05)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Rule {self.machine.machine_id}: Temp Max = {self.max_temperature}°C"
