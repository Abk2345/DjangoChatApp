from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignUpForm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.utils import timezone
from .serializers import UserSerializer
from django.http import HttpResponse

# Create your views here.
def frontpage(request):
    return render(request, 'chat/frontpage.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            return redirect('frontpage')
    else:
        form = SignUpForm()

    return render(request, 'chat/signup.html', {'form': form})

from django.contrib.auth.views import LoginView
from .forms import CustomAuthenticationForm  # Import the custom form

class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm  # Use the custom form
    template_name = 'chat/login.html'  # Your login template
