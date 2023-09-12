from django.urls import path, re_path

from . import consumers

websocket_urlpatterns = [
    path('ws/<str:room_name>/', consumers.ChatConsumer.as_asgi()),
    path('ws/chat/<str:friend_name>/', consumers.PersonalChatConsumer.as_asgi()),
]
