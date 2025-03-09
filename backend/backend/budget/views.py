from backend.models import Budget
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from backend.budget.serializers import BudgetSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_budget(request):
    """
    Create a new budget
    """
    serializer = BudgetSerializer(data=request.data)
    if serializer.is_valid():
        budget = serializer.save()
        return Response(BudgetSerializer(budget).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_budget(request):
    """
    Update an existing budget
    """
    # Ensure the 'id' is included in the request data
    if 'id' not in request.data:
        return Response({'detail': 'Budget ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

    # Retrieve the budget by the provided 'id' from the request data
    try:
        budget = Budget.objects.get(pk=request.data['id'])
    except Budget.DoesNotExist:
        return Response({'detail': 'Budget not found.'}, status=status.HTTP_404_NOT_FOUND)

    # Create the serializer with the existing budget instance and the updated data
    serializer = BudgetSerializer(budget, data=request.data)

    # Check if the data is valid
    if serializer.is_valid():
        updated_budget = serializer.save()  # Save the updated budget
        return Response(BudgetSerializer(updated_budget).data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_budget(request, id):
    """
    Get budget by id
    """
    try:
        budget = Budget.objects.get(pk=id)
    except Budget.DoesNotExist:
        return Response({'detail': 'Budget not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = BudgetSerializer(budget)

    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_budget(request, id):
    """
    Delete a budget
    """
    try:
        budget = Budget.objects.get(pk=id)
        budget.delete()
        return Response(status=status.HTTP_200_OK)
    except Budget.DoesNotExist:
        return Response({'detail': 'Budget not found.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_current_budgets(request):
    """
    Get all current budgets (budgets with no end date)
    """
    budgets = Budget.objects.filter(end_date__isnull=True)
    
    # Serialize the result
    serializer = BudgetSerializer(budgets, many=True)
    
    return Response(serializer.data)

