from django.db import models
from django.utils import timezone

# Create your models here.
class PlaceCache(models.Model):
    address = models.CharField(max_length=100)
    distance = models.FloatField()
    last_update = models.DateTimeField(default=timezone.now)
