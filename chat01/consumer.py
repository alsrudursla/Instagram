import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from chat01.models import Chatting


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.commands[data['command']](self, data)

    # Receive message from WebSocket
    async def new_messages(self, text_data):
        text_data_json = text_data

        message = text_data_json["message"]
        from_user = text_data_json["from_user"]
        to_user = text_data_json["to_user"]
        room_id = text_data_json["room_id"]

        await self.save_message(to_user, from_user, message, room_id)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "from_user": from_user, "message": message}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        from_user = event["from_user"]
        # Send message to WebSocket
        await self.send(text_data=json.dumps({"command":"receive_message", "from_user": from_user, "message": message}))

    @database_sync_to_async
    def save_message(self, to, from_user, message, room_id):
        chatting = Chatting()
        chatting.to = to
        chatting.from_user = from_user
        chatting.message = message
        chatting.room_id = room_id
        return chatting.save()

    # 저장된 메세지 불러오기
    async def return_message(self, data):
        messages = await self.return_db()
        content = {
            'command': 'return_messages',
            'messages': messages
        }

        await self.send(text_data=json.dumps(content))

    @database_sync_to_async
    def return_db(self):
        result = Chatting.objects.filter(room_id=self.room_name)
        messages = []

        for message in result:
            messages.append({'to_user': message.to, 'from_user': message.from_user, 'message': message.message})
        return messages

    commands = {
        'return_messages': return_message,
        'new_messages': new_messages
    }
