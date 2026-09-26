# core-api/tenants/models.py

from django.db import models

class Tenant(models.Model):
    tenant_id = models.CharField(max_length=50, unique=True, primary_key=True)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.tenant_id})"