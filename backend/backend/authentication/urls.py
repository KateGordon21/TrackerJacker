# authentication/urls.py
from django.urls import path
from .views import (
    register,
    login,
    user_details,
    logout,
    delete_user,
    update_user,
    get_user_by_id,
    get_user_by_username
)

urlpatterns = [
    path('register/', register, name='auth_register'),
    path('login/', login, name='auth_login'),
    path('user/', user_details, name='user_details'),
    path('logout/', logout, name='auth_logout'),
    path('delete/', delete_user, name="auth_delete_user"),
    path('update/', update_user, name='auth_update'),
    
    # First the integer ID, then the string username to avoid conflicts
    path('get/<int:id>/', get_user_by_id, name='get_user_by_id'),
    path('get/<str:username>/', get_user_by_username, name='get_user_by_username'),
]
