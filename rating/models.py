from django.db import models
from django.contrib.auth.models import User
from food.models import Food  # Adjust the import path accordingly

class Rating(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.food.name} - {self.rating} by {self.user.username}"