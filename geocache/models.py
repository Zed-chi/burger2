from django.db import models
from django.utils import timezone


# Create your models here.
class Place(models.Model):
    address = models.CharField("Адрес", max_length=100)
    lat = models.FloatField("Широта")
    lon = models.FloatField("Долгота")
    last_update = models.DateTimeField("Дата последнего обновления", default=timezone.now)

    def __str__(self) -> str:
        return f"{self.lat} - {self.lon}"