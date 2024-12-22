from django.urls import path
from rating.views import create_rating, rated_foods, show_json, show_xml, create_rating_flutter, edit_rating, delete_rating, edit_rating_flutter, delete_rating_flutter
from .views import get_rating_ajax, edit_rating_ajax, delete_rating_ajax

app_name = 'rating'

urlpatterns = [
    path('rate/<int:food_id>/', create_rating, name='create_rating'),
    path('rated-foods/', rated_foods, name='rated_foods'),
    path('json/', show_json, name='get_json'),
    path('xml/', show_xml, name='get_xml'),
    path('create_rating_flutter/', create_rating_flutter, name='create_rating_flutter'),
    path('edit-rating/<uuid:rating_id>/', edit_rating, name='edit_rating'),
    path('delete-rating/<uuid:rating_id>/', delete_rating, name='delete_rating'),
    path('edit-rating-flutter/<uuid:rating_id>/', edit_rating_flutter, name='edit_rating_flutter'),
    path('delete-rating-flutter/<uuid:rating_id>/', delete_rating_flutter, name='delete_rating_flutter'),
    path('get_rating_ajax/<uuid:rating_id>/', get_rating_ajax, name='get_rating_ajax'),
    path('edit_rating_ajax/', edit_rating_ajax, name='edit_rating_ajax'),
    path('delete_rating_ajax/', delete_rating_ajax, name='delete_rating_ajax'),
]