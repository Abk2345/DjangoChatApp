from django.urls import path

from . import views

urlpatterns = [
    path("suggest/<int:user_id>", views.get_suggested_friends, name='suggest-friends'),
]