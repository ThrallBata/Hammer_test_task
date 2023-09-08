from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Profile
from .serializers import ProfileSerializer
from .tasks import send_authcode
from .utils import create_auth_code, redis_auth_code, redis_jwt, redis_refresh_token, token_jwt


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

    code_redis = redis_auth_code.get(phone)
    if code_redis:
        code_redis = code_redis.decode("utf-8")
        if code_redis == authcode:
            profile = Profile.object.get(phone=phone)
            token = token_jwt(profile.phone)
            token_refresh = token_jwt(profile.phone, 'refresh')
            print(token, 'token')
            print(token_refresh, 'reftoken')
            return Response(ProfileSerializer(
                {'phone': profile.phone, 'invite_code': profile.invite_code, 'token': token, 'token_refresh': token_refresh}, ).data)

    return Response({'error': 'неверные данные',}, status=status.HTTP_400_BAD_REQUEST)


# TODO продумать и сделать рефреш токен-систему и дальнейший функционал


@api_view(['POST'])
def authenticate_refresh_tokenAPIView(request):
    refresh_token = request.data.get('refresh_token')
    ...
