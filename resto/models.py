from django.db import models
from food.models import Food

class Resto(models.Model):
    nama = models.CharField(max_length=30)
    makanan = models.ForeignKey(Food, on_delete=models.CASCADE)
    lokasi = models.CharField(max_length=30)