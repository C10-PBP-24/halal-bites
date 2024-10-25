from django.urls import path
from food.views import show_menu, food_detail, add_food, get_food, get_food_by_id, filter_food

app_name = 'food'

urlpatterns = [
    path('', show_menu, name='menu'),
    path('food_detail/<int:food_id>/', food_detail, name="food_detail"),
    path('get_food/', get_food, name='get_food'),
    path('get_food/<int:id>/', get_food_by_id, name='get_food_by_id'),
    path('add_food/', add_food, name='add_food'),
    path('filter_food/', filter_food, name='filter_food')
]