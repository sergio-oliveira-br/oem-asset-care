# core-api/machines/models.py

from django.db import models
from tenants.models import Tenant

class Machine(models.Model):
    machine_id = models.CharField(max_length=50, primary_key=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='machines')
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.machine_id} - {self.tenant.tenant_id}"
