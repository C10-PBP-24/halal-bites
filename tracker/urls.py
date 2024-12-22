from django.urls import path
from . import views

app_name = 'tracker'

urlpatterns = [
    path('json/', views.show_json, name='show_json'),
    path('add/', views.add_tracker, name='add_tracker'),
]