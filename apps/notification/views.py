from django.shortcuts import render
from rest_framework.views import APIView
#from rest_framework_mongoengine.viewsets import ModelViewSet
from rest_framework.exceptions import NotFound
from rest_framework import status
from .models import Notification
from userinfo.models import UserInfo, User
from docs.models import DetailDocument
from rest_framework import status
from django.core.exceptions import SuspiciousOperation
from .customResponse import CustomResponse
from .serializer import NotificationSerializer, NotificationCreateSerializer
from .consumer import NotifConsumer
import json
from datetime import datetime
from userinfo.views import authenticate_credentials
# Create your views here.


class NotificationView(APIView):

    def get_object(self, user):
        #try:
        data_notif =Notification.objects.filter(to=user).order_by('-create_date')[:5]
        list_notif=[]
        for dn in data_notif:
            json_dict = {}
            if dn.detail:
                #json_detail = eval(dn.detail)
                json_detail = json.loads(dn.detail)
                data_detaildoc=DetailDocument.objects.get(id=json_detail['detaildoc_id'])
                if data_detaildoc.status=='active':
                    json_dict['id']=dn.id
                    json_dict['fromm']=dn.fromm
                    json_dict['to']=dn.to
                    json_dict['type']=dn.type
                    json_dict['title']=dn.title
                    json_dict['message']=dn.message
                    json_dict['detail']=dn.detail
                    json_dict['status']=dn.status
                    json_dict['create_date']=dn.create_date
                    json_dict['update_date']=dn.update_date
                    list_notif.append(json_dict)
        return list_notif
        # return Notification.objects.filter(to=user).order_by('-create_date')[:5] 
        # except Notification.DoesNotExist:
        #     raise Http404('Notif Not Found')

    def get(self, request, user):
        try:
            token = request.META.get("HTTP_AUTHORIZATION").replace(" ", "")[6:]
            ret1,userT = authenticate_credentials(token)
            if False == ret1 or None ==userT:
                return CustomResponse().badRequest(
                    message='token invalid'
                )
            userId = user
            if not userId:
                raise SuspiciousOperation('Need Param User')
            user = User.objects.get(id=userId)
            if not user:
                raise NotFound('User Not Found')
            data = self.get_object(user.id)
            serializer = NotificationSerializer(data, many=True)
            json_dict={}
            list_data=[]
            for s in serializer.data:
                json_dict['id']=s['id']
                json_dict['fromm']=s['fromm']
                json_dict['to']=s['to']
                json_dict['type']=s['type']
                json_dict['title']=s['title']
                json_dict['message']=s['message']
                json_dict['detail']=json.loads(s['detail'])
                json_dict['status']=s['status']
                json_dict['create_date']=s['create_date']
                json_dict['update_date']=s['update_date']
                list_data.append(json_dict)
            # return CustomResponse.ok(values=serializer.data)
            return CustomResponse.ok(values=list_data)
        except NotFound as e:
            return CustomResponse().base(message=str(e), status=status.HTTP_404_NOT_FOUND)
        except SuspiciousOperation as e:
            return CustomResponse.badRequest(message=str(e))
        except Exception as e:
            return CustomResponse().base(success=False, message=str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            token = request.META.get("HTTP_AUTHORIZATION").replace(" ", "")[6:]
            ret1,user = authenticate_credentials(token)
            if False == ret1 or None ==user:
                return CustomResponse().badRequest(
                    message='token invalid'
                )
            id = request.data.get('id')
            # serializer = NotificationCreateSerializer(data=request.data)
            # if serializer.is_valid():
            #     serializer.save()
            #     return CustomResponse().base(values=serializer.data, status=status.HTTP_201_CREATED)
            # return CustomResponse.badRequest(serializer.errors)
            notif = NotifConsumer()
            notif.send_message(to=id, message='hai')
        except NotFound as e:
            return CustomResponse().base(message=str(e), status=status.HTTP_404_NOT_FOUND)
        except SuspiciousOperation as e:
            return CustomResponse.badRequest(message=str(e))
        except Exception as e:
            return CustomResponse().base(success=False, message=str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request):
        try:
            token = request.META.get("HTTP_AUTHORIZATION").replace(" ", "")[6:]
            ret1,user = authenticate_credentials(token)
            if False == ret1 or None ==user:
                return CustomResponse().badRequest(
                    message='token invalid'
                )
            id = request.data.get('id')
            try:
                notif = Notification.objects.get(id=id)
            except Notification.DoesNotExist:
                raise Http404('Notif Not Found')
            
            notif.status = 'open'
            notif.update_date = datetime.now() #datetime.now
            notif.save()
            return CustomResponse().ok(message="Notif Success")
        except NotFound as e:
            return CustomResponse().base(message=str(e), status=status.HTTP_404_NOT_FOUND)
        except SuspiciousOperation as e:
            return CustomResponse.badRequest(message=str(e))
        except Exception as e:
            return CustomResponse().base(success=False, message=str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
