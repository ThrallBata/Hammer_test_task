from django.urls import path, include, re_path

from .views import authenticate_phoneAPIView


urlpatterns = [
    path('auth/', authenticate_phoneAPIView),
]
