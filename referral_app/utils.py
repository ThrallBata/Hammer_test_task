import random
from datetime import timedelta

import jwt
import redis

from django.conf import settings


redis_auth_code = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=1)
redis_jwt = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=2)
redis_refresh_token = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=3)


def create_auth_code(phone):
    code = random.randint(1000, 9999)
    redis_auth_code.setex(str(phone), timedelta(minutes=5), value=str(code))
    # print(f'время жизни кода аутентификации: {redis_auth_code.ttl(str(phone))}')

    return code


def get_tokens(phone):
    return {'jwt': token_jwt(phone), 'refresh': token_refresh(phone)}


def token_jwt(phone):
    lifetime = settings.JWT_TOKEN_LIFETIME
    token = _generate_jwt_token(phone, lifetime)
    redis_jwt.setex(phone, timedelta(hours=int(lifetime)), value=token)

    return token


def token_refresh(phone):
    days = settings.REFRESH_TOKEN_LIFETIME
    lifetime = int(days) * 24

    token = _generate_refresh_token()
    redis_refresh_token.setex(phone, timedelta(hours=int(lifetime)), value=token)

    return token


def _generate_jwt_token(phone, lifetime):

    token = jwt.encode({
        'phone': phone,
        'lifetime': f"{lifetime} hours"
    }, settings.SECRET_KEY, algorithm='HS256')

    return token


def _generate_refresh_token():
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890@!#$%^&*.'
    token_list = []
    n = random.randint(35, 40)

    for i in range(n):
        token_list.append(random.choice(chars))

    refresh_token = ''.join(token_list)

    return refresh_token
