import os
import uuid
import django
from channels.routing import get_default_application

def get_local_mac():
    return uuid.uuid1().hex[-12:]

def isRight():
    mac = get_local_mac()
    #print(mac)
    #if mac == "3035ada97ba4":
    return 1
    #print("error 403")
    #return 0

if isRight():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fs_server.settings")
    django.setup()
    application = get_default_application()
