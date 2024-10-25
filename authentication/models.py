from django.db import models
from django.contrib.auth.models import AbstractUser
from rating.models import Rating
from tracker.models import FoodTracker

class CustomUser(AbstractUser):
    USER_ROLE_CHOICES = [
        ('user', 'User'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=5, choices=USER_ROLE_CHOICES, default='user')
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.username

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    rated_foods = models.ManyToManyField(Rating, related_name="rated_foods")
    tracked_foods = models.ManyToManyField(FoodTracker, related_name="tracked_foods")

    def __str__(self):
        return self.full_name