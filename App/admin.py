from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import ApplianceClass, ApplianceType

admin.site.register(ApplianceClass)
admin.site.register(ApplianceType)