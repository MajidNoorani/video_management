from channels.generic.websocket import AsyncWebsocketConsumer
import json


class ProgressConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)
        # Handle received data here

    async def send_progress(self, progress):
        await self.send(text_data=json.dumps({
            'progress': progress
        }))


# from channels.generic.websocket import AsyncWebsocketConsumer
# import json


# class VideoUploadConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()

#     async def disconnect(self, close_code):
#         pass

#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']

#         await self.send(text_data=json.dumps({
#             'message': message
#         }))


# import json
# from channels.generic.websocket import AsyncWebsocketConsumer


# class VideoUploadConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.user = self.scope["user"]
#         self.upload_group_name = f'upload_{self.user.sub}'

#         # Join room group
#         await self.channel_layer.group_add(
#             self.upload_group_name,
#             self.channel_name
#         )

#         await self.accept()

#     async def disconnect(self, close_code):
#         # Leave room group
#         await self.channel_layer.group_discard(
#             self.upload_group_name,
#             self.channel_name
#         )

#     # Receive message from WebSocket
#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']

#         # Send message to room group
#         await self.channel_layer.group_send(
#             self.upload_group_name,
#             {
#                 'type': 'upload_progress',
#                 'message': message
#             }
#         )

#     # Receive message from room group
#     async def upload_progress(self, event):
#         message = event['message']

#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({
#             'message': message
#         }))
