from django.urls import path
from resto.views import get_resto, show_resto, filter_resto, add_resto
from resto.views import delete_resto, resto_detail, show_json
from django.contrib.auth.decorators import login_required


app_name = "resto"

urlpatterns = [
    path('', login_required(show_resto, login_url='/auth/login'), name='show_resto'),
    path('filter-resto/', filter_resto, name='filter_resto'),
    path('add-resto/', add_resto, name='add_resto'),
    path('delete-resto/<int:id>/', delete_resto, name="delete_resto"),
    path('detail/<int:pk>/', resto_detail, name="resto_detail"),
]