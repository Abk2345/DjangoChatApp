import json

from channels.generic.websocket import AsyncWebsocketConsumer

from asgiref.sync import sync_to_async

from .models import Message, Room, PersonalMessage

from django.contrib.auth.models import User

from datetime import datetime

class ChatConsumer(AsyncWebsocketConsumer):
    # print("Reached here?")
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        print("data recieved", data)
        message = data['message']
        username = data['username']
        room = data['room']

        await self.save_message(username, room, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'room': room,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        room = event['room']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'room': room,
        }))

    @sync_to_async
    def save_message(self, username, room, message):
        user = User.objects.get(username=username)
        room = Room.objects.get(slug=room)

        Message.objects.create(user=user, room=room, content=message)

# personal-chat/consumers.py
from .models import PersonalMessage

class PersonalChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['url_route']['kwargs']['friend_name']
        self.room_name = f"user_{self.user}"
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive(self, text_data):
        print("In receiver", text_data)
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        receiver_username = text_data_json['receiver_username']
        sender_username = text_data_json['sender_username']

        # Store the message in the database
        await self.save_message(sender_username, receiver_username, message)
        
        # Send the message to the receiver's personal chat room
        room_name = f"user_{receiver_username}"
        await self.channel_layer.group_send(
            room_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_username': sender_username,
            }
        )

        room_name = f"user_{sender_username}"
        await self.channel_layer.group_send(
            room_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_username': sender_username,
            }
        )
        

    async def chat_message(self, event):
        message = event['message']
        sender_username = event['sender_username']

        await self.send(text_data=json.dumps({
            'message': message,
            'sender_username': sender_username,
        }))
    
    @sync_to_async
    def save_message(self, sender_username, receiver_username, message):
          # Find the receiver by username
        
        sender = User.objects.get(username=sender_username)
        receiver = User.objects.get(username=receiver_username)
        PersonalMessage.objects.create(sender=sender, recipient=receiver, content=message)



