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
        #ch_group_list = channel_layer.groups.copy()
        #print(ch_group_list)
        id = self.scope['url_route']['kwargs']['id']
        if not id:
            self.close()
        #for x, y in ch_group_list.items():
        #    if self.channel_name in y.keys():
        #        async_to_sync(self.channel_layer.group_discard)(
        #            x, self.channel_name)
        async_to_sync(self.channel_layer.group_add)(
            'digidoc', self.channel_name)
        # self.channel_layer.group_add(
        #     id, self.channel_name)
        self.accept()
        print('====connect ws==== '+id)

    def disconnect(self, close_code):
        # ch_group_list = channel_layer.groups.copy()
        # for x, y in ch_group_list.items():
        #     if self.channel_name in y.keys():
        #         async_to_sync(self.channel_layer.group_discard)(
        #             x, self.channel_name)
        id = self.scope['url_route']['kwargs']['id']
        #r = redis.Redis(host='127.0.0.1', port=6379, db=0)
        # r = redis.StrictRedis('127.0.0.1', 6379, charset="utf-8", decode_responses=True)
        # print(r.keys('*'))
        # if r.exists('asgi:group:'+id):
        #     print('ASUUUU')
        # print(r.get('asgi:group:digidoc'))
        async_to_sync(self.channel_layer.group_discard)('digidoc', self.channel_name)
        # await self.channel_layer.group_discard(id, self.channel_name)
        print('====disconnect ws===='+id)
        # raise StopConsumer()


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
            'digidoc',
            {"type": 'send_message_to_frontend', 'message': message}
        )

    def send_message_to_frontend(self, event):
        message = event['message']
        self.send(text_data=json.dumps({
            'message': message
        }))
