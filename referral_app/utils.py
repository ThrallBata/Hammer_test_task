import random
from datetime import timedelta

import jwt
import redis

from django.conf import settings


redis_auth_code = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=1)
redis_jwt = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=2)


def create_auth_code(phone):
    code = random.randint(1000, 9999)
    redis_auth_code.setex(str(phone), timedelta(minutes=5), value=str(code))
    # print(f'время жизни кода аутентификации: {redis_auth_code.ttl(str(phone))}')

    return code


def token_jwt(phone):
    return _generate_jwt_token(phone)


def _generate_jwt_token(phone):

    token = jwt.encode({
        'phone': phone,
    }, settings.SECRET_KEY, algorithm='HS256')

    redis_jwt.setex(phone, timedelta(hours=2), value=token)
    return token
