from django.db import models
from datetime import datetime
from userinfo.models import User
# Create your models here.


class Notification(models.Model):
    fromm = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    to = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='to')
    type = models.CharField(max_length=45)
    title = models.CharField(max_length=45)
    message = models.CharField(max_length=500)
    detail = models.TextField(blank=True, null=True)
    #status = models.StringField(required=True, choices=[ 'new', 'open'], default='new')
    status = models.CharField(max_length=45, default='new')

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)
    
    meta = {
        'collection': 'notification',
        'ordering': ['-create_date']
    }
