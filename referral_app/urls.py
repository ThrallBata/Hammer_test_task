from django.urls import path, include, re_path

from .views import *


urlpatterns = [
    path('auth/', authenticate_phoneAPIView),
    path('auth/code_entry/', authenticate_codeAPIView),
    path('auth/refresh/', authenticate_refresh_tokenAPIView),
]
