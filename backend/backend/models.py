from django.db import models
from django.contrib.auth.models import User


class Budget(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()

class Category(models.Model):
    name = models.CharField(max_length=100)
    start_amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_amount = models.DecimalField(max_digits=10, decimal_places=2)

    budget = models.ForeignKey(Budget, related_name='categories', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'budget')

class Expense(models.Model):
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    store = models.CharField(max_length=100)
    payback_amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    notes = models.CharField(max_length=5000)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='expenses')

class UserBudgetMap(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'budget')

