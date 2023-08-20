from django.urls import path, include, re_path

from .views import authenticateAPIView


urlpatterns = [
    path('users/', authenticateAPIView),
]
