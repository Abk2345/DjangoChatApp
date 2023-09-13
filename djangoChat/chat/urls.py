from django.urls import path
from django.contrib.auth import views as auth_views

from django.contrib.auth.views import LoginView
from .forms import CustomAuthenticationForm


from . import views

urlpatterns = [
    path('login/', LoginView.as_view(
        template_name='chat/login.html',
        authentication_form=CustomAuthenticationForm  #using custom form from forms.py
        ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('', views.frontpage, name='frontpage'),
]
