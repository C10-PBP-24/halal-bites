from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Food(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Resto(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.name

class Rating(models.Model):
    score = models.IntegerField()
    comment = models.TextField(blank=True)

    def clean(self):
        if not (1 <= self.score <= 5):
            raise ValidationError('Score must be between 1 and 5.')
    def __str__(self):
        return f"{self.score} - {self.comment}"


class Tracker(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Resto, on_delete=models.CASCADE)
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE)
    order_at = models.DateTimeField()

    def __str__(self):
        return f"{self.food.name} at {self.restaurant.name} - Rated {self.rating.score} by {self.user.username}"
