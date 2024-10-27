from django.db import models
from food.models import Food
from resto.models import Resto
from rating.models import Rating
from django.conf import settings
import uuid

class Tracker(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=uuid.uuid4)
    restaurant = models.ForeignKey(Resto, on_delete=models.CASCADE)
    order_at = models.DateTimeField() 

    def __str__(self):
        return f"{self.food.name} at {self.restaurant.nama} - Rated {self.rating.rating} by {self.user.username}"
