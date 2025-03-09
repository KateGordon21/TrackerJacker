from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class UserAuthTests(APITestCase):

    password = "mypass12345"
    
    # Registration Tests
    def test_register_user_success(self):
        data = {
            'username': 'testuser',
            'password': self.password,
            'password2': self.password,
        }
        response = self.client.post('/api/auth/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('user', response.data)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['user']['username'], 'testuser')
        response = self.client.post('/api/auth/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_user_password_mismatch(self):
        data = {
            'username': 'testuserpasswordmistmatch',
            'password': self.password,
            'password2': 'password456',
        }
        response = self.client.post('/api/auth/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    # Login Tests
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser1',
            password=self.password,
        )
        self.token, created = Token.objects.get_or_create(user=self.user)  # Ensure token creation


    def test_login_user_success(self):
        data = {
            'username': 'testuser1',
            'password': self.password,
        }
        response = self.client.post('/api/auth/login/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('user', response.data)

    def test_login_invalid_credentials(self):
        data = {
            'username': 'testuser1',
            'password': 'wrongpassword',
        }
        response = self.client.post('/api/auth/login/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Invalid credentials')

    # User Details Tests
    def test_user_details(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key) 
        self.client.login(username='testuser1', password=self.password)
        response = self.client.get('/api/auth/user/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser1')

    def test_user_details_not_authenticated(self):
        self.client.logout()
        response = self.client.get('/api/auth/user/', format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Logout Tests
    def test_logout_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key) 
        self.client.login(username='testuser1', password=self.password)
        token = Token.objects.get(user=self.user)
        self.assertEqual(token.user, self.user)
        
        response = self.client.post('/api/auth/logout/', format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Check that the token was deleted
        with self.assertRaises(Token.DoesNotExist):
            Token.objects.get(user=self.user)

    # New Tests for Get User by ID
    def test_get_user_by_id_success(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key) 
        response = self.client.get(f'/api/auth/get/{self.user.id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser1')

    def test_get_user_by_id_not_found(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key) 
        response = self.client.get('/api/auth/get/9999/', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'User not found.')

    # New Tests for Get User by Username
    def test_get_user_by_username_success(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key) 
        response = self.client.get(f'/api/auth/get/{self.user.username}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser1')

    def test_get_user_by_username_not_found(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key) 
        response = self.client.get('/api/auth/get/nonexistentuser/', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'User not found.')

    # New Test for Update User Details
    def test_update_user_success(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key) 
        data = {'username': 'updateduser'}
        response = self.client.put('/api/auth/update/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'updateduser')

    def test_update_user_not_authenticated(self):
        response = self.client.put('/api/auth/update/', {'username': 'newuser'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_user_invalid_data(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key) 
        data = {'username': ''}  # Invalid data (empty username)
        response = self.client.put('/api/auth/update/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def tearDown(self):
        # Delete the user and any associated tokens after the test
        if hasattr(self, 'user') and self.user:
            self.user.delete()
