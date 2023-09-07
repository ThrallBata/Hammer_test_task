from datetime import datetime

import redis

from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Profile, AuthCode
from .serializers import ProfileSerializer
from .tasks import send_authcode
from .utils import create_auth_code, redis_auth_code

redis_jwt = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=2)


@api_view(['POST'])
def authenticate_phoneAPIView(request):   # получения номера телефона, создание и отправка кода
    phone = request.data.get('phone')
    profile_queryset = Profile.object.filter(phone=phone)

    # TODO проверка валидности номера телефона при отправке

    if profile_queryset.exists():
        pass
        # profile = profile_queryset[0]
    else:
        profile = Profile.object.create_profile(phone)

    authcode = create_auth_code(phone)
    print('Отправка кода на телефон')
    send_authcode.delay(phone, authcode)

    return Response({}, status=status.HTTP_200_OK)


@api_view(['POST'])
def authenticate_codeAPIView(request):
    authcode = request.data.get('authcode')
    phone = request.data.get('phone')

    print(authcode)

    code_redis = redis_auth_code.get(phone).decode("utf-8")
    if code_redis:
        print(code_redis)
        if code_redis == authcode:
            profile = Profile.object.get(phone=phone)

            # TODO как проверить, что номер существует без доп запроса в базу

            # token = Profile.token(profile)
            return Response(ProfileSerializer(
                {'phone': profile.phone, 'invite_code': profile.invite_code, 'token':"111"}, ).data)

        return Response({'error': 'неверный код', }, status=status.HTTP_400_BAD_REQUEST)

    # if authcode_queryset.exists():
    #     date_now = datetime.now()
    #     for authcode_elem in authcode_queryset:
    #         if authcode_elem.end_date > date_now:
    #             print(authcode_elem.profile)
    #             profile = Profile.object.get(phone=authcode_elem.profile)
    #             token = Profile.token(profile)
    #             return Response(ProfileSerializer(
    #                 {'phone': profile.phone, 'invite_code': profile.invite_code, 'token': token}, ).data)
    # else:
    #     return Response({}, status=status.HTTP_400_BAD_REQUEST)
    return Response({}, status=status.HTTP_400_BAD_REQUEST)





