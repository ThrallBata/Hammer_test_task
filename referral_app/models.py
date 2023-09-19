import random

from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import RegexValidator
from django.db import models


class ProfileManager(BaseUserManager):
    def create_profile(self, phone):
        if phone is None:
            raise TypeError('Users must have a phone number.')

        profile = self.model(phone=phone, invite_code=generate_invite_code(6))
        profile.save()

        return profile


class Profile(models.Model):
    phone_regex = RegexValidator(
        regex=r'^((\+7|7|8)+([0-9]){10})$',
        message="Phone number must be entered in the format: '+79*********'."
    )
    phone = models.CharField(validators=[phone_regex], max_length=17, verbose_name='Номер телефона')
    invite_code = models.CharField(max_length=6, null=False, verbose_name='Код приглашения')
    inviter = models.CharField(max_length=6, null=True, verbose_name='Код пригласившего')

    object = ProfileManager()

    def __str__(self):
        return self.phone


def generate_invite_code(n: int) -> str:
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    invite_code_list = []

    for i in range(n):
        invite_code_list.append(random.choice(chars))

    invite_code = ''.join(invite_code_list)

    """Проверка на уникальность инвайткода. Если код существует, функция вызовется снова,
     если код уникальный вернет значение """
    is_non_unique = Profile.object.filter(invite_code=invite_code).exists()
    if is_non_unique:
        generate_invite_code(n)
    else:
        return invite_code



