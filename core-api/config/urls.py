"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tenants.views import create_tenant
from machines.views import register_machine
from alert_configs.views import update_threshold

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/tenants/', create_tenant, name='create_tenant'),
    path('api/v1/machines/', register_machine, name='register_machine'),
    path('api/v1/machines/<str:machine_id>/thresholds/', update_threshold, name='update_threshold'),
]
