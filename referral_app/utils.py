import random
from datetime import timedelta

import redis

from django.conf import settings

# from .models import Profile


redis_auth_code = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=1)


def create_auth_code(phone):
    code = random.randint(1000, 9999)
    redis_auth_code.setex(str(phone), timedelta(minutes=5), value=str(code))
    print(f'время жизни кода аутентификации: {redis_auth_code.ttl(str(phone))}')

    return code

# def generate_invite_code() -> str:
#     chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
#     invite_code_list = []
#
#     for i in range(6):
#         invite_code_list.append(random.choice(chars))
#
#     invite_code = ''.join(invite_code_list)
#
#     """Проверка на уникальность инвайткода. Если код существует, функция вызовется снова,
#      если код уникальный вернет значение """
#     is_non_unique = Profile.object.filter(invite_code=invite_code).exists()
#     if is_non_unique:
#         generate_invite_code()
#     else:
#         return invite_code
