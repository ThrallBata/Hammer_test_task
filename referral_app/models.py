import random

from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import User


class ProfileManager(BaseUserManager):
    def create_profile(self, phone):
        if phone is None:
            raise TypeError('Users must have a phone number.')

        profile = self.model(phone=phone, invite_code=generate_invite_code())
        profile.save()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=30, null=False, verbose_name='Номер телефона')
    invite_code = models.CharField(max_length=6, null=False, verbose_name='Код приглашения')
    code_usage = models.BooleanField(default=False)
    inviter = models.CharField(max_length=6, null=True, verbose_name='Код пригласившего')

    object = ProfileManager()

    def __str__(self):
        return self.phone


def generate_invite_code() -> str:
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    invite_code_list = []

    for i in range(6):
        invite_code_list.append(random.choice(chars))

    invite_code = ''.join(invite_code_list)

    """Проверка на уникальность инвайткода. Если код существует, функция вызовется снова,
     если код уникальный вернет значение """
    is_non_unique = Profile.objects.filter(invite_code=invite_code).exists()
    if is_non_unique:
        generate_invite_code()
    else:
        return invite_code






