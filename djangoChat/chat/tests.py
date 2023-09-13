from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

# Total 7 Tests: 3 api's

#Test Api 1:  testing login functionality -> Contains 3 tests, right template test, valid credentials test, invalid credentials test
class LoginViewTest(TestCase):
    def setUp(self):
        # Create a test user
        self.username = 'testuser'
        self.password = 'testpass123'
        self.user = User.objects.create_user(username=self.username, password=self.password)


    def test_login_view(self):
        # # request to the login page with url
        login_url = reverse('login')
        response = self.client.get(login_url)

        # ok?
        self.assertEqual(response.status_code, 200)

        # correct template used?
        self.assertTemplateUsed(response, 'chat/login.html')

    def test_login_valid_credentials(self):
        

        # test login data
        login_data = {
            'username': self.username,
            'password': self.password,
        }

        # post request to the login with valid credentials
        login_url = reverse('login')        
        response = self.client.post(login_url, data=login_data)

        # redirect?
        self.assertEqual(response.status_code, 302)

        # authenticated?
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_invalid_credentials(self):

        # invalid login test data
        invalid_login_data = {
            'username': self.username,
            'password': 'wrongpassword',
        }

        # post request with invalid credentials
        login_url = reverse('login')
        response = self.client.post(login_url, data=invalid_login_data)

        # ok?
        self.assertEqual(response.status_code, 200)

        # not authenticated?
        self.assertFalse(response.wsgi_request.user.is_authenticated)


# Test Api 2: Signup -> contains 3 tests: right template test, valid data test, invalid data test
class SignupViewTest(TestCase):
    def test_signup_view(self):
        #get request to the signup page
        signup_url = reverse('signup')
        response = self.client.get(signup_url)

        # ok?
        self.assertEqual(response.status_code, 200)

        # signup template?
        self.assertTemplateUsed(response, 'chat/signup.html')

    def test_signup_valid_data(self):
        # valid data
        signup_data = {
            'username': 'testuser',
            'password1': 'testpass123',
            'password2': 'testpass123',
        }

        # post request with valid data
        signup_url = reverse('signup')
        response = self.client.post(signup_url, data=signup_data)

        # redirect?
        self.assertEqual(response.status_code, 302)

        # authenticated?
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_signup_invalid_data(self):
        # invalid signup data
        invalid_signup_data = {
            'username': 'testuser',
            'password1': 'testpass123',
            'password2': 'wrongpassword',
        }

        #post request with invalid data
        signup_url = reverse('signup')
        response = self.client.post(signup_url, data=invalid_signup_data)

        # ok?
        self.assertEqual(response.status_code, 200)

        # not authenticated?
        self.assertFalse(response.wsgi_request.user.is_authenticated)


# Log out Api Test: Contains 1 test, redirection to home and not authenticated afterwards
class LogoutViewTest(TestCase):
    def setUp(self):
        # Create a test user and log them in
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.login(username='testuser', password='testpass123')

    def test_logout_view(self):
        # get request to the logout page
        logout_url = reverse('logout')
        response = self.client.get(logout_url)

        # ok?
        self.assertEqual(response.status_code, 302)

        # logged out , not authenticated?
        self.assertFalse(response.wsgi_request.user.is_authenticated)
