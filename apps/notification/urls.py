from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('notif/', views.NotificationView.as_view()),
    path('notif/<str:user>', views.NotificationView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
