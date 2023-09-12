# from django.test import TestCase

# # Create your tests here.
# import requests
# import unittest

# from django.test import Client

# from django.urls import reverse
# from django.contrib.auth.models import User
# from .forms import SignUpForm

# from django.contrib.auth.models import User

# class APITestCase(TestCase):
#     def setUp(self):
#         self.client = Client()
#         # when running with signup tests, it is not required
#         self.user = User.objects.create_user(
#             username='testuser5',
#             password='testpass123',
#         )
    
    # def test_signup(self):
    #     # Create a user dictionary with valid data
    #     user_data = {
    #         'username': 'testuser',
    #         'password1': 'testpass123',
    #         'password2': 'testpass123',
    #     }

    #     # Make a POST request to the signup view
    #     response = self.client.post(reverse('signup'), data=user_data)

    #     # Assert that the user was created
    #     self.assertEqual(response.status_code, 302)  # Check for a redirect
    #     self.assertTrue(User.objects.filter(username='testuser').exists())

#     def test_login(self):
#         # Valid login data
#         valid_login_data = {
#             'username': 'testuser',
#             'password': 'testpass123',
#         }

#         # Invalid login data with an incorrect password
#         invalid_password_data = {
#             'username': 'testuser',
#             'password': 'wrongpassword',
#         }

#         # Invalid login data with a non-existing username
#         invalid_username_data = {
#             'username': 'nonexistentuser',
#             'password': 'testpass123',
#         }

#         # POST request to the login view with valid credentials
#         url = reverse('login')
#         response_valid = self.client.get(url, data=valid_login_data)
#         self.assertEqual(response_valid.status_code, 302)
#         self.assertRedirects(response_valid, reverse('home'))  # Correct redirection
#         self.assertTrue(response_valid.wsgi_request.user.is_authenticated)

#         # POST request with invalid password
#         response_invalid_password = self.client.post(url, data=invalid_password_data)
#         self.assertEqual(response_invalid_password.status_code, 200)  # Unsuccessful login
#         self.assertFalse(response_invalid_password.wsgi_request.user.is_authenticated)

#         # POST request with invalid username
#         response_invalid_username = self.client.post(url, data=invalid_username_data)
#         self.assertEqual(response_invalid_username.status_code, 200)  # Unsuccessful login
#         self.assertFalse(response_invalid_username.wsgi_request.user.is_authenticated)

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class LoginViewTest(TestCase):
    def setUp(self):
        # Create a test user
        self.username = 'testuser'
        self.password = 'testpass123'
        self.user = User.objects.create_user(username=self.username, password=self.password)


    def test_login_view(self):
        # Define the URL for the login view
        login_url = reverse('login')

        # Make a GET request to the login page
        response = self.client.get(login_url)

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the 'login' template is used
        self.assertTemplateUsed(response, 'chat/login.html')

    def test_login_valid_credentials(self):
        # Define the URL for the login view
        login_url = reverse('login')

        # Prepare login data with valid credentials
        login_data = {
            'username': self.username,
            'password': self.password,
        }

        # Make a POST request to the login view with valid credentials
        response = self.client.post(login_url, data=login_data)

        # Check if the response status code is 302 (redirect)
        self.assertEqual(response.status_code, 302)

        # Check if the user is authenticated
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_invalid_credentials(self):
        # Define the URL for the login view
        login_url = reverse('login')

        # Prepare login data with invalid password
        invalid_login_data = {
            'username': self.username,
            'password': 'wrongpassword',
        }

        # Make a POST request to the login view with invalid credentials
        response = self.client.post(login_url, data=invalid_login_data)

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the user is not authenticated
        self.assertFalse(response.wsgi_request.user.is_authenticated)


class SignupViewTest(TestCase):
    def test_signup_view(self):
        # Define the URL for the signup view
        signup_url = reverse('signup')

        # Make a GET request to the signup page
        response = self.client.get(signup_url)

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the 'signup' template is used
        self.assertTemplateUsed(response, 'chat/signup.html')

    def test_signup_valid_data(self):
        # Define the URL for the signup view
        signup_url = reverse('signup')

        # Prepare signup data with valid credentials
        signup_data = {
            'username': 'testuser',
            'password1': 'testpass123',
            'password2': 'testpass123',
        }

        # Make a POST request to the signup view with valid data
        response = self.client.post(signup_url, data=signup_data)

        # Check if the response status code is 302 (redirect)
        self.assertEqual(response.status_code, 302)

        # Check if the user is authenticated after signup
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_signup_invalid_data(self):
        # Define the URL for the signup view
        signup_url = reverse('signup')

        # Prepare signup data with invalid password confirmation
        invalid_signup_data = {
            'username': 'testuser',
            'password1': 'testpass123',
            'password2': 'wrongpassword',
        }

        # Make a POST request to the signup view with invalid data
        response = self.client.post(signup_url, data=invalid_signup_data)

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the user is not authenticated after invalid signup
        self.assertFalse(response.wsgi_request.user.is_authenticated)


class LogoutViewTest(TestCase):
    def setUp(self):
        # Create a test user and log them in
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.login(username='testuser', password='testpass123')

    def test_logout_view(self):
        # Define the URL for the logout view
        logout_url = reverse('logout')

        # Make a GET request to the logout page
        response = self.client.get(logout_url)

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 302)

        # Check if the user is logged out
        self.assertFalse(response.wsgi_request.user.is_authenticated)
