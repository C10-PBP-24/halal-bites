from django.urls import path
from . import views

urlpatterns = [
    path('tracker/', views.food_tracker, name='food_tracker'),
    path('tracker/add/', views.add_food_tracking, name='add_food_tracking'),
]
