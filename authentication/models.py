import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    USER_ROLE_CHOICES = [
        ('user', 'User'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=5, choices=USER_ROLE_CHOICES, default='user')

    def __str__(self):
        return self.username

class UserProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    rated_foods = models.ManyToManyField('rating.Rating', related_name="rated_foods")
    tracked_foods = models.ManyToManyField('tracker.Tracker', related_name="tracked_foods")

    def __str__(self):
        return self.user.username