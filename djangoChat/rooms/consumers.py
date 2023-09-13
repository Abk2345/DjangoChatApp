import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Message, Room, PersonalMessage
from django.contrib.auth.models import User
from datetime import datetime

# For chat rooms, chatconsumer
class ChatConsumer(AsyncWebsocketConsumer):
    # print("Reached here?")
    # called after websocket connect is made
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # adding channel to room's group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

        # accepting connection
        await self.accept()

    # called when connection is closed
    async def disconnect(self, code):
        # removing channel from user's group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # called when message is received by websocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        # print("data recieved", data)
        message = data['message']
        username = data['username']
        room = data['room']

        await self.save_message(username, room, message)

        # adding message to room's group witht help of channel
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'room': room,
            }
        )

    # called when message is sent by user
    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        room = event['room']

        # sending message back to webscoket to broadcast
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'room': room,
        }))

    # saving message synchronously to database
    @sync_to_async
    def save_message(self, username, room, message):
        user = User.objects.get(username=username)
        room = Room.objects.get(slug=room)

        Message.objects.create(user=user, room=room, content=message)


# Extending Chat Rooms for personal chat usecase
from .models import PersonalMessage

class PersonalChatConsumer(AsyncWebsocketConsumer):
    # called when websocket connection is established
    async def connect(self):
        self.user = self.scope['url_route']['kwargs']['friend_name']
        self.room_name = f"user_{self.user}"

        # adding websocket channel to room's group
        await self.channel_layer.group_add(self.room_name, self.channel_name)

        #accepting connection
        await self.accept()

    # called when connection is closed
    async def disconnect(self, close_code):
        # removing channel from room's group
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    # called when message is recieved by websocket
    async def receive(self, text_data):
        print("In receiver", text_data)
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        receiver_username = text_data_json['receiver_username']
        sender_username = text_data_json['sender_username']

        # Saving message in the database
        await self.save_message(sender_username, receiver_username, message)
        
        # Sending message to the receiver's personal chat room for realtime update
        room_name = f"user_{receiver_username}"
        await self.channel_layer.group_send(
            room_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_username': sender_username,
            }
        )

        # Sending message to the sender's personal chat room for real-time update
        room_name = f"user_{sender_username}"
        await self.channel_layer.group_send(
            room_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_username': sender_username,
            }
        )
        
    # called when a message is sent from user
    async def chat_message(self, event):
        message = event['message']
        sender_username = event['sender_username']

        # sending message back to websocket to broadcast
        await self.send(text_data=json.dumps({
            'message': message,
            'sender_username': sender_username,
        }))
    
    # Synchronous function to save the message to the database
    @sync_to_async
    def save_message(self, sender_username, receiver_username, message):
        # sender and receiver by username
        sender = User.objects.get(username=sender_username)
        receiver = User.objects.get(username=receiver_username)
        PersonalMessage.objects.create(sender=sender, recipient=receiver, content=message)



