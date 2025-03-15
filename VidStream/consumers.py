import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.urls import path

class RoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_code = self.scope['url_route']['kwargs']['room_code']
        self.room_group_name = f'room_{self.room_code}'

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json['action']
        time = text_data_json['time']

        # Send message to room group
        await self.channel_layer.group_send(self.room_group_name, {'type': 'sync_video', 'action': action, 'time': time})

    async def sync_video(self, event):
        action = event['action']
        time = event['time']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({'action': action, 'time': time}))

# Define your WebSocket URL patterns in the same file
websocket_urlpatterns = [
    path('ws/room/<str:room_code>/', RoomConsumer.as_asgi()),  # Define your WebSocket path
]