from django.urls import path
from .views import register, user_login, logout_view
from .views import login, register_flutter, logout_flutter, get_user_info

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', logout_view, name='logout'),
    path('login-flutter/', login, name='login_flutter'),
    path('register-flutter/', register_flutter, name='register_flutter'),
    path('logout-flutter/', logout_flutter, name='logout_flutter'),
    path('user-info/', get_user_info, name='get_user_info'),
]