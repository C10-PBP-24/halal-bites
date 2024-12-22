from django.db import models
from food.models import Food
from resto.models import Resto
from django.conf import settings

class Tracker(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    order_at = models.DateTimeField()  # Tetap gunakan field ini

    def __str__(self):
        return f"{self.food.name} ordered by {self.user.username}"
