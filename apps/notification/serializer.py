#from rest_framework_mongoengine.serializers import DocumentSerializer
#from rest_framework_mongoengine.serializers import serializers
from rest_framework import serializers
from .models import Notification
from userinfo.models import UserInfo, User


class NotifUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        # exclude = ('password', )
        depth = 1


class NotificationSerializer(serializers.ModelSerializer):
    # from_ = NotifUserSerializer(many=True, read_only=True)
    # to = NotifUserSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = '__all__'
        depth = 1


class NotificationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
        depth = 0
