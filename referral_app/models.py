import random

from datetime import datetime, timedelta
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.conf import settings

import jwt


class ProfileManager(BaseUserManager):
    def create_profile(self, phone):
        if phone is None:
            raise TypeError('Users must have a phone number.')

        profile = self.model(phone=phone, invite_code=generate_invite_code())
        profile.save()

        return profile


class Profile(models.Model):
    phone = models.CharField(max_length=30, null=False, verbose_name='Номер телефона')
    invite_code = models.CharField(max_length=6, null=False, verbose_name='Код приглашения')
    code_usage = models.BooleanField(default=False)
    inviter = models.CharField(max_length=6, null=True, verbose_name='Код пригласившего')

    object = ProfileManager()

    def __str__(self):
        return self.phone

    # @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):

        dt = datetime.now() + timedelta(days=1)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token


class AuthCodeManager(BaseUserManager):
    def create_auth_code(self, profile):
        code = random.randint(1000, 9999)
        init_date = datetime.now()
        end_date = datetime.now() + timedelta(minutes=5)

        code = self.model(profile=profile, code=code, init_date=init_date, end_date=end_date)
        code.save()

        return code


class AuthCode(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Пользователь')
    code = models.IntegerField(null=False)
    init_date = models.DateTimeField(editable=False)
    end_date = models.DateTimeField(editable=False)

    object = AuthCodeManager()


def generate_invite_code() -> str:
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    invite_code_list = []

    for i in range(6):
        invite_code_list.append(random.choice(chars))

    invite_code = ''.join(invite_code_list)

    """Проверка на уникальность инвайткода. Если код существует, функция вызовется снова,
     если код уникальный вернет значение """
    is_non_unique = Profile.object.filter(invite_code=invite_code).exists()
    if is_non_unique:
        generate_invite_code()
    else:
        return invite_code






