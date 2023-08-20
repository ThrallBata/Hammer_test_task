from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Profile
from .serializers import ProfileSerializer


@api_view(['POST'])
def authenticateAPIView(request):
    phone = request.data.get('phone')

    if Profile.object.filter(phone=phone).exists():
        token = Profile.token(Profile)
        return Response(ProfileSerializer({'phone': phone, 'invite_code': Profile.invite_code, 'token': token }, ).data)
    else:
        Profile.object.create_profile(phone)
        token = Profile.token(Profile)

        return Response(ProfileSerializer({'phone': phone, 'invite_code': Profile.invite_code, 'token': token }, ).data)




