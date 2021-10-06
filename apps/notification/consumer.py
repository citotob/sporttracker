# websocket

from asgiref.sync import async_to_sync

from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
import json
from userinfo.models import User #UserInfo, 
import random
import threading
import asyncio
from channels.exceptions import StopConsumer

from channels.layers import get_channel_layer
import redis
channel_layer = get_channel_layer()


class NotifConsumer(WebsocketConsumer):
    def connect(self):
        id = self.scope['url_route']['kwargs']['id']
        if not id:
            self.close()
        async_to_sync(self.channel_layer.group_add)(
            'sporttracker', self.channel_name)
        self.accept()
        print('====connect ws==== '+id)

    def disconnect(self, close_code):
        id = self.scope['url_route']['kwargs']['id']
        async_to_sync(self.channel_layer.group_discard)('sporttracker', self.channel_name)
        print('====disconnect ws===='+id)


    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        async_to_sync(self.channel_layer.send)(
            self.channel_name,
            {"type": 'send_message_to_frontend', 'message': message}
        )

    def send_message(self, to, message):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'sporttracker',
            {"type": 'send_message_to_frontend', 'message': message}
        )

    def send_message_to_frontend(self, event):
        message = event['message']
        self.send(text_data=json.dumps({
            'message': message
        }))
