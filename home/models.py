from django.db import models


class Sensor(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    sunlight = models.DecimalField(max_digits=5, decimal_places=2)
    humidity = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        ordering = ('date',)

    def __str__(self):
        return self.date
