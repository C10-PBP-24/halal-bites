from django.urls import path
from . import views

app_name = 'tracker'

urlpatterns = [
    path('food_tracker', views.food_tracker, name='food_tracker'),
    path('json/', views.show_json, name='show_json'),
    path('add/', views.add_tracker, name='add_tracker'),
]
