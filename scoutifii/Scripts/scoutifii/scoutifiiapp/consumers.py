import json

from .models import Room, Messaging, Profile

from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        
        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
    
    async def receive(self, text_data):
        text_json_data = json.loads(text_data)
        message = text_json_data
        event = {
            'type': 'send_message',
            'message': message
        }
        
        await self.channel_layer.group_send(self.room_name, event)
    
    async def disconnect(self, close_code):
        # leave room
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
    
    async def send_message(self, event):
        data = event['message']
        await self.create_message(data=data)
        response_data = {
            'created_by': data['created_by'],
            'message_body': data['message_body']
        }
        await self.send(text_data=json.dumps({'message': response_data}))
    
    @database_sync_to_async
    def create_message(self, data):
        get_room_by_name = Room.objects.get(room=data['room'])
        
        if not Messaging.objects.filter(message_body=data['message_body']).exists():
            new_message = Messaging(room=get_room_by_name, profile=data['profile'], sent_by=data['sent_by'], created_by=data['created_by'], message_body=data['message_body'])
            new_message.save()
        