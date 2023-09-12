from time import sleep

from celery import shared_task


@shared_task()
def send_authcode(phone, code):
    sleep(3)
    print(f'Код для аутентификации на номер {phone}: {code}')