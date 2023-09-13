from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# sign up form based on default django UserCreationForm, with three choosen fields, password2 is for confirming password1 while signup
class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

from django.contrib.auth.forms import AuthenticationForm

#customized authentication form using django base Authentication form to show error in login properly
class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        'invalid_login': "Your credentials are not correct. Please try again.",
    }