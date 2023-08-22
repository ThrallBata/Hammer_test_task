from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Profile, AuthCode
from .serializers import ProfileSerializer


@api_view(['POST'])
def authenticate_phoneAPIView(request): #  получения номера телефона, создание и отправка кода
    phone = request.data.get('phone')

    #TODO проверка валидности номера телефона к авторизациям

    if Profile.object.filter(phone=phone).exists():
        profile_queryset = Profile.object.filter(phone=phone)
        profile = profile_queryset[0]
    else:
        profile = Profile.object.create_profile(phone)

    authcode = AuthCode.object.create_auth_code(profile)

    print(f'Отправка кода на телефон: {authcode.code}')

    return Response({}, status=status.HTTP_200_OK)


# @api_view(['POST'])
# def authenticateAPIView_2(request):
#     phone = request.data.get('phone')
#
#     if Profile.object.filter(phone=phone).exists():
#         profile_queryset = Profile.object.filter(phone=phone)
#         profile = profile_queryset[0]
#     else:
#         profile = Profile.object.create_profile(phone)
#
#     token = Profile.token(profile)
#     return Response(ProfileSerializer({'phone': profile.phone, 'invite_code': profile.invite_code, 'token': token}, ).data)





