from django.db import models


class Sensor(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    temperature = models.CharField(max_length=30)
    sunlight = models.CharField(max_length=30)
    humidity = models.CharField(max_length=30)

    def __str__(self):
        return self.date
