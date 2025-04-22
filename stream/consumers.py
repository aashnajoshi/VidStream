import json
from channels.generic.websocket import AsyncWebsocketConsumer

class RoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_code = self.scope['url_route']['kwargs']['room_code']
        self.room_group_name = f"room_{self.room_code}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get("action")
        time = data.get("time")

        # Broadcast play, pause, seek to group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "sync_event",
                "action": action,
                "time": time,
            }
        )

    async def sync_event(self, event):
        # Send the event back to all clients 
        await self.send(text_data=json.dumps({
            "action": event["action"],
            "time": event.get("time"),
        }))