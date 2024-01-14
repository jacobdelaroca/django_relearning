# chat/consumers.py
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ExclusiveRoom

from channels.consumer import AsyncConsumer


class ChatConsumerNew(AsyncWebsocketConsumer):
    async def connect(self):
        print('connected', self.scope['user'], self.scope['url_route']['kwargs']['room_name'])
        room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{room_name}"
        user = self.scope['user']
        user1, user2 = await self.get_users(room_name)
        print(user1.username, user2.username, user.username)
        accepted = True
        if(user1 == user):
            await self.accept()
        elif user1 == user2 and not user == user2:
            await self.set_user2(room_name=room_name, user2=user)
            await self.accept()
        elif user2 == user:
            await self.accept()
        else:
            print('rejected')
            await self.close()
            accepted = False
        if accepted: await self.channel_layer.group_add(self.room_group_name, self.channel_name)
    
    @database_sync_to_async
    def get_users(self, room_name):
        room = ExclusiveRoom.objects.get(room_name=room_name)
        return room.user1, room.user2
    @database_sync_to_async
    def set_user2(self, room_name=None, user2=None):
        room = ExclusiveRoom.objects.get(room_name=room_name)
        room.user2 = user2
        print(room.user2.username)
        room.save()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        print(message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message}
        )


    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))
    
    

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": message}
        )


    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))