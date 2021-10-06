from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from rest_framework.routers import DefaultRouter

count_data = views.webcamAPI.as_view({
    'post': 'send_count'
})

urlpatterns = [
    path('count/', count_data),
]

urlpatterns = format_suffix_patterns(urlpatterns)