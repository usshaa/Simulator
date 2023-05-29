from django.db import models

class SensorData(models.Model):
    pressure = models.FloatField()
    temperature = models.FloatField()
    flow_rate = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"SensorData - {self.timestamp}"

class FailureData(models.Model):
    pressure = models.FloatField()
    temperature = models.FloatField()
    flow_rate = models.FloatField()
    is_failure = models.BooleanField()

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Failure Data - ID: {self.id}"