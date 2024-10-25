from django.db import models
from food.models import Food

class Resto(models.Model):
    nama = models.CharField(max_length=30)
    makanan = models.CharField(max_length=100)
    lokasi = models.CharField(max_length=30)