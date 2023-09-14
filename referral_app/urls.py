from django.urls import path, include, re_path

from .views import *


urlpatterns = [
    path('auth/', authenticate_phoneAPIView, name='login_create'),
    path('auth/code_entry/', authenticate_codeAPIView, name='entry_by_code'),
    path('auth/refresh/', authenticate_refresh_tokenAPIView, name='refresh_token'),

    path('activate_code/', activate_invite_codeAPIView, name='activate_code'),
    path('invited_profiles/', show_who_activated_invite_codeAPIView, name='activate_code'),

]
