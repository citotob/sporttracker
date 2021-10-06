from django.shortcuts import render
from django.http import JsonResponse
from userinfo.models import UserInfo, User, UserSession
from docs.models import Log
from django.contrib.sessions.models import Session
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from rest_framework.authtoken.models import Token
import json
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, timedelta
#from .customResponse import CustomResponse
#from rest_framework import status
from .response import Response
import requests
from rest_framework import viewsets
from rest_framework import status
from .serializer import UserSerializer


def check_conn(request):
    # if request.method == 'POST':
    # try:
    return Response.ok(
        values=[],
        message='True'
    )
    #     except Exception as e:
    #         return CustomResponse().base(success=False, message=str(e), status=500)
    # else:
    #     return CustomResponse().base(success=False, message='Post Only', status=500)


def remove_other_sessions(sender, user, request, **kwargs):
    # remove other sessions
    Session.objects.filter(usersession__user=user).delete()
    #try:
    # save current session
    request.session.save()

    # create a link from the user to the current session (for later removal)
    UserSession.objects.get_or_create(
        user=user,
        session=Session.objects.get(pk=request.session.session_key)
    )
    # except:
    #     pass

def login(request):
    # if request.method == 'POST':
    #     try:
    #req = request.body.decode("utf-8")
    #data = json.loads(req)
    token = request.META.get("HTTP_AUTHORIZATION").replace(" ", "")[6:]
    ret1, user = authenticate_credentials(token)
    if False == ret1 or None == user:
        return Response.badRequest(
            values=[],
            message='token invalid'
        )
    """
    secret_key = settings.RECAPTCHA_SECRET_KEY

    # captcha verification
    d = {
        'response': data.get('g-recaptcha-response'),
        'secret': secret_key
    }
    resp = requests.post('https://www.google.com/recaptcha/api/siteverify', data=d)
    result_json = resp.json()

    #print(result_json)

    if not result_json.get('success'):
        return Response.badRequest(
            values=[],
            message='recaptcha salah'
        )
    # end captcha verification
    """
    # d = {
    #     'username':request.POST.get('email'),
    #     'password':request.POST.get('password')
    # }
    # #resp = requests.post('http://hqnappsiptl.bpk.go.id:8071/api/UserAD/verifylogin', data=d)
    # #result_json = resp.json()

    # resp = requests.post('http://hqnappsiptl.bpk.go.id:8071/api/UserAD/verifylogin', json=d)
    # #print(resp.status_code)
    # #print(resp.json())

    # if resp.status_code==401:
    #     return Response.badRequest(
    #         values=[],
    #         message='wrong data'
    #     )
    # data_litbang = resp.json()
    try:
        data_user = User.objects.get(
            email=request.POST.get('email'), status="aktif")
        if data_user.current_log:
            past = data_user.current_log + timedelta(hours=4)
            if past > datetime.now():
                return Response.badRequest(
                    values=[],
                    message='someone has logged in'
                )
        # if request.session[request.session.session_key]:
        #     return Response.badRequest(
        #         values=[],
        #         message='someone has logged in'
        #     )
        # try:
        #     print(request.session[str(data_user.id)])
        #     # del request.session[str(data_user.id)]
        #     return Response.badRequest(
        #         values=[],
        #         message='someone has logged in'
        #     )
        # except:
        #     pass
        data_user.last_log = datetime.now()  # datetime.utcnow()
        data_user.current_log = datetime.now()
        # data_user.name = data_litbang['nama']
    except User.DoesNotExist:
        data_user = None
    if not data_user:
        data_user = User(
            username=request.POST.get('email'),
            email=request.POST.get('email'),
            # name = data_litbang['nama'],
            status='aktif',
            current_log=datetime.now()
        )
    data_user.save()
    # request.session[str(data_user.id)] = data_user.id
    # request.session[request.session.session_key]
    #remove_other_sessions(data_user,data_user,request)
    return Response.ok(
        values=data_user.serialize(),
        message='Login Success'
    )
    #     except Exception as e:
    #         return CustomResponse().base(success=False, message=str(e), status=500)
    # else:
    #     return CustomResponse().base(success=False, message='Post Only', status=500)


def logout(request):
    token = request.META.get("HTTP_AUTHORIZATION").replace(" ", "")[6:]
    ret1, user = authenticate_credentials(token)
    if False == ret1 or None == user:
        return Response.badRequest(
            values=[],
            message='token invalid'
        )
    try:
        data_user = User.objects.get(
            email=request.POST.get('email'), status="aktif")

        data_user.current_log = None
        data_user.save()
        # del request.session[str(data_user.id)]
    except User.DoesNotExist:
        return Response.badRequest(
            values=[],
            message='user not found'
        )

    return Response.ok(
        values=data_user.serialize(),
        message='Logout Success'
    )
    #     except Exception as e:
    #         return CustomResponse().base(success=False, message=str(e), status=500)
    # else:
    #     return CustomResponse().base(success=False, message='Post Only', status=500)


def authenticate_credentials(key):
    from rest_framework.authtoken.models import Token
    model = Token
    try:
        token = model.objects.select_related('user').get(key=key)
    except model.DoesNotExist:
        #raise exceptions.AuthenticationFailed(_('Invalid token.'))
        return False, None

    if not token.user.is_active:
        #raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))
        return False, None
    userinfo = UserInfo.objects.get(id=token.user_id)
    return True, userinfo


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
        password = instance.password
        if instance.username != "admin":
            instance.set_password(password)  # Password encryption method
        instance.save()


def getActive(request):
    token = request.META.get("HTTP_AUTHORIZATION").replace(" ", "")[6:]
    ret1, userT = authenticate_credentials(token)
    if False == ret1 or None == userT:
        return Response.badRequest(
            values=[],
            message='token invalid'
        )
    #users = User.objects.filter(status='aktif')
    log_users = Log.objects.values_list('user')
    log_users = list(set(log_users))
    log_userss = []
    for lu in log_users:
        log_userss.append(lu[0])
    users = User.objects.filter(status='aktif',pk__in=log_userss)
    serializer = UserSerializer(users, many=True)

    return Response.ok(
        values=serializer.data
    )
