from django.db import models

class ApplianceClass(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class ApplianceType(models.Model):
    appliance_class = models.ForeignKey(ApplianceClass, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
