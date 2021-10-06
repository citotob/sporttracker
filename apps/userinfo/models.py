from django.db import models
from django.contrib.auth.models import AbstractUser
import random
from django.contrib.sessions.models import Session


class UserInfo(AbstractUser):
    nickname = models.CharField(max_length=30,default="Rooster", blank=True, null=True, verbose_name='nickname')
    betcoin = models.CharField(max_length=128,default="[0,0,0,0,0,0,0,0,0]", blank=True, null=True, verbose_name='Bet on gold coins')
    coin =models.BigIntegerField(default=0, verbose_name='Number of gold coins')
    diamond = models.BigIntegerField(default=0, verbose_name='Number of diamonds')
    level =models.BigIntegerField(default=0, verbose_name='grade')
    code = models.CharField(max_length=30,default="0000", verbose_name='Invitation code')
    class Meta:
        verbose_name = 'User Management'
        verbose_name_plural = verbose_name
        ordering = ['-level']
	
    def __str__(self):
        return self.username

class User(models.Model):
    username = models.CharField(max_length=30, blank=False, null=False, unique=True)
    name = models.CharField(max_length=500, blank=True, null=True)
    email = models.EmailField(max_length=254, blank=False, null=False, unique=True)
    role = models.CharField(max_length=30, blank=True, null=True)
    edit_text = models.BooleanField(default=False, blank=True, null=True)
    status = models.CharField(max_length=30, blank=True, null=True)
    first_log = models.DateTimeField(auto_now_add=True)
    last_log = models.DateTimeField(auto_now_add=True)
    current_log = models.DateTimeField(blank=True, null=True)
	
    def __str__(self):
        return self.username

    def serialize(self):
        return {
            "id": str(self.id),
            "username": self.username,
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "edit_text": self.edit_text,
            "status": self.status,
            "first_log": self.first_log,
            "last_log": self.last_log,
            "current_log": self.current_log
        }

class UserSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.OneToOneField(Session, on_delete=models.CASCADE)

class AppVersion(models.Model):
    mobile = models.CharField(max_length=20,default="1", verbose_name='MobileVersion', unique=True)
    web = models.CharField(max_length=20,default="1", verbose_name='WebVersion', unique=True)
    