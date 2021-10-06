from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import FileUploadParser
from .customResponse import CustomResponse
from notification.utils.CustomNotification import CustomNotification
import json

class webcamAPI(viewsets.ModelViewSet):
    def send_count(self, request, format=None):
        #push_count = request.query_params.get('count', None)
        #confidence = request.query_params.get('confidence', None)
        req = request.body.decode("utf-8")
        data = json.loads(req)
        push_count = data.get('count', None)
        conf = data.get('conf', None)
        json_doc = {}
        json_doc['count'] = push_count
        json_doc['conf'] = conf
        notif = CustomNotification()
        notif.create(to=1, from_=1, type='send_count',
                    title='send_count', message='send_count' , push_message='Ada pesan baru',
                    detail=json.dumps(json_doc))
        return CustomResponse().base(values=[], status=status.HTTP_201_CREATED)