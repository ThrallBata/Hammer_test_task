from django.urls import path, include, re_path

from .views import authenticate_phoneAPIView, authenticate_codeAPIView


urlpatterns = [
    path('auth/', authenticate_phoneAPIView),
    path('auth/code_entry/', authenticate_codeAPIView),
]
