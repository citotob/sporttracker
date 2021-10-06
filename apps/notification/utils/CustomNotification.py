from notification.models import Notification
from notification.serializer import NotificationCreateSerializer
from rest_framework.exceptions import ValidationError
from notification.consumer import NotifConsumer

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import asyncio
import multiprocessing
import threading


class CustomNotification():

    def create(self, from_, to, type, title, message, push_message, detail):
        data = {
            "fromm": from_,
            "to": to,
            "type": type,
            "title": title,
            "message": message,
            "detail": detail
        }
        serializer = NotificationCreateSerializer(data=data)

        # def send_message_to_frontend(self, event):
        #     message = event['message']
        #     self.send(text_data=json.dumps({
        #         'message': message
        #     }))

        def send_async(message):
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                str(to),
                {"type": 'send_message_to_frontend', 'message': message}
            )
            
        if serializer.is_valid():
            serializer.save()

            channel_layer = get_channel_layer()
            #for x in to:
            # channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'digidoc',
                {"type": 'send_message_to_frontend', 'message': message}
            )
            # fork = multiprocessing.Process(target=send_async(message))
            # fork.start()
            # fork.join()
            # x = threading.Thread(
            #             target=send_async(message), args=(message,))

            return serializer.data

        raise ValidationError(serializer.errors)
