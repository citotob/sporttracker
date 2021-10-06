from django.urls import path
from userinfo import views
from rest_framework.authtoken import views as tokenview

urlpatterns = [
    path('token/', tokenview.obtain_auth_token),
    path('login/', views.login),
    path('logout/', views.logout),
    path('check_conn/', views.check_conn),
    path('get/active/', views.getActive),

]
