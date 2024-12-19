from django.urls import path
from rating.views import create_rating, rated_foods, show_json, show_xml

app_name = 'rating'

urlpatterns = [
    path('rate/<int:food_id>/', create_rating, name='create_rating'),
    path('rated-foods/', rated_foods, name='rated_foods'),
    path('json/', show_json, name='get_json'),
    path('xml/', show_xml, name='get_xml'),
]