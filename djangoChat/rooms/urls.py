from django.urls import path

from . import views

urlpatterns = [
    path('online-users/', views.get_active_users, name='online-users'),
    path('rooms/', views.rooms, name='rooms'),
    path('', views.home, name='home'),
    path('start/<str:username>/', views.personalChatUser, name='personal-chat'),
    path('<slug:slug>/', views.room, name='room'),
    
]
