from django.urls import path
from rating.views import create_rating, rated_foods, show_json, show_xml, create_rating_flutter, edit_rating, delete_rating

app_name = 'rating'

urlpatterns = [
    path('rate/<int:food_id>/', create_rating, name='create_rating'),
    path('rated-foods/', rated_foods, name='rated_foods'),
    path('json/', show_json, name='get_json'),
    path('xml/', show_xml, name='get_xml'),
    path('create_rating_flutter/', create_rating_flutter, name='create_rating_flutter'),
    path('edit-rating/<uuid:rating_id>/', edit_rating, name='edit_rating'),
    path('delete-rating/<uuid:rating_id>/', delete_rating, name='delete_rating'),
]