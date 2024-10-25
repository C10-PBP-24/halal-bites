from django.urls import path
from resto.views import get_resto, show_resto

app_name = "resto"

urlpatterns = [
    path("", get_resto, name="get_resto"),
    path("show-resto", show_resto, name="show_resto")
]