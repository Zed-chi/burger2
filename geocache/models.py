from django.db import models
from django.utils import timezone


# Create your models here.
class PlaceCache(models.Model):
    address = models.CharField("Адрес", max_length=100)
    distance = models.FloatField("Расстояние")
    last_update = models.DateTimeField("Дата последнего обновления", default=timezone.now)
