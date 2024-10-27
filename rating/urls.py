from django.urls import path
from rating.views import create_rating, rated_foods

app_name = 'rating'

urlpatterns = [
    path('rate/<int:food_id>/', create_rating, name='create_rating'),
    path('rated-foods/', rated_foods, name='rated_foods'),
]