# serializers.py

from rest_framework import serializers
from backend.models import Budget

class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ['id', 'name', 'start_date', 'end_date']
