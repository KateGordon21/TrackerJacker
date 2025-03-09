from django.urls import path
from .views import (
    create_budget,
    update_budget,
    get_budget,
    delete_budget,
    get_all_current_budgets,
)

urlpatterns = [
    path('create/', create_budget, name='create_budget'),
    path('update/', update_budget, name='update_budget'),
    path('get/<int:id>/', get_budget, name='get_budget'),
    path('delete/<int:id>/', delete_budget, name='delete_budget'),
    path('get_all_current/', get_all_current_budgets, name='get_all_current_budgets'),
]
