from django.test import TestCase
from rest_framework import status
from backend.models import Budget
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from datetime import date

class BudgetTests(TestCase):

    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        
        # Get the authentication token for the user
        self.token = Token.objects.create(user=self.user)
        
        # Initialize the API client and authenticate
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    # Test creating a budget
    def test_create_budget_success(self):
        data = {
            'name': 'Test Budget',
            'start_date': '2025-01-01',
            'end_date': '2025-12-31',
        }
        response = self.client.post('/api/budget/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Test Budget')
        self.assertEqual(response.data['start_date'], '2025-01-01')
        self.assertEqual(response.data['end_date'], '2025-12-31')

    # Test creating a budget without a name (bad request)
    def test_create_budget_missing_name(self):
        data = {
            'start_date': '2025-01-01',
            'end_date': '2025-12-31',
        }
        response = self.client.post('/api/budget/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)

    # Test updating a budget
    def test_update_budget_success(self):
        # First, create a budget
        budget = Budget.objects.create(
            name='Test Budget',
            start_date='2025-01-01',
            end_date='2025-12-31',
        )
        data = {
            'id': budget.id,
            'name': 'Updated Budget',
            'start_date': '2025-01-01',
            'end_date': '2025-12-31',
        }
        response = self.client.post('/api/budget/update/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Budget')

    # Test updating a non-existing budget
    def test_update_budget_not_found(self):
        data = {
            'id': 9999,  # Non-existing ID
            'name': 'Updated Budget',
            'start_date': '2025-01-01',
            'end_date': '2025-12-31',
        }
        response = self.client.post('/api/budget/update/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Budget not found.')

    # Test getting a budget
    def test_get_budget_success(self):
        # First, create a budget
        budget = Budget.objects.create(
            name='Test Budget',
            start_date='2025-01-01',
            end_date='2025-12-31',
        )
        response = self.client.get(f'/api/budget/get/{budget.id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Budget')

    # Test getting a non-existing budget
    def test_get_budget_not_found(self):
        response = self.client.get('/api/budget/get/9999/', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Budget not found.')

    # Test deleting a budget
    def test_delete_budget_success(self):
        # First, create a budget
        budget = Budget.objects.create(
            name='Test Budget',
            start_date='2025-01-01',
            end_date='2025-12-31',
        )
        response = self.client.delete(f'/api/budget/delete/{budget.id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if the budget is deleted
        with self.assertRaises(Budget.DoesNotExist):
            Budget.objects.get(id=budget.id)

    # Test deleting a non-existing budget
    def test_delete_budget_not_found(self):
        response = self.client.delete('/api/budget/delete/9999/', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Budget not found.')

    # Test getting all current budgets
    def test_get_all_current_budgets(self):
        # Create some budgets
        budget1 = Budget.objects.create(
            name='Test Budget 1',
            start_date='2025-01-01',
            end_date=None,  # Ongoing budget
        )
        budget2 = Budget.objects.create(
            name='Test Budget 2',
            start_date='2025-01-01',
            end_date='2025-12-31',
        )

        response = self.client.get('/api/budget/get_all_current/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only 1 ongoing budget (budget1)
        self.assertEqual(response.data[0]['name'], 'Test Budget 1')

    # Test getting all current budgets when there are no ongoing budgets
    def test_get_all_current_budgets_empty(self):
        # Create a budget with an end date
        Budget.objects.create(
            name='Completed Budget',
            start_date='2020-01-01',
            end_date='2020-12-31',
        )

        response = self.client.get('/api/budget/get_all_current/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)  # No ongoing budgets

    # Test creating a budget with invalid date format
    def test_create_budget_invalid_date_format(self):
        data = {
            'name': 'Test Budget',
            'start_date': '2025-01-01',  # Valid date
            'end_date': 'invalid-date',  # Invalid date
        }
        response = self.client.post('/api/budget/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('end_date', response.data)

    # Test that budget data cannot be empty
    def test_create_budget_empty_data(self):
        data = {}
        response = self.client.post('/api/budget/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test that only authenticated users can create budgets
    def test_create_budget_not_authenticated(self):
        self.client.credentials()  # Remove the authentication credentials
        data = {
            'name': 'Test Budget',
            'start_date': '2025-01-01',
            'end_date': '2025-12-31',
        }
        response = self.client.post('/api/budget/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
