# authentication/urls.py

from django.urls import path
from .views import register, login, user_details, logout, delete_user

urlpatterns = [
    path('register/', register, name='auth_register'),
    path('login/', login, name='auth_login'),
    path('user/', user_details, name='user_details'),
    path('logout/', logout, name='auth_logout'),
    path('delete/', delete_user, name="auth_delete_user"),
]
