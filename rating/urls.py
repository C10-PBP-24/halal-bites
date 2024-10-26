from django.urls import path
from .views import create_rating, show_rating_form

urlpatterns = [
    path('rate/<int:food_id>/', create_rating, name='create_rating'),
    path('show/', show_rating_form, name='show_rating_form'),
]