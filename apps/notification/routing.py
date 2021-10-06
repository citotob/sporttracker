from django.urls import re_path, path
from django.conf.urls import url
from .consumer import NotifConsumer

websocket_urlpatterns = [
   re_path("ws/(?P<id>\w+)", NotifConsumer.as_asgi()),
]

# websocket_urlpatterns = [
#      re_path('ws/(?P<id>\w+)', NotifConsumer),
# ]

# websocket_urlpatterns = [
#   url(r'^ws/(?P<id>\w+)/$', NotifConsumer),
# ]