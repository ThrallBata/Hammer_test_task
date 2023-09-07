# Phone number authentication

## Для запуска сервиса необходимо :
Установленный Python 3.10, Postgres 14, Redis 6.
0. Склонировать репозиторий
1. Установить зависимости `pip install -r requirements.txt`
2. Необходимо указать свои данные в файле **.env** для подключения к БД и сделать миграции `python manage.py migrate`.
3. Необходимо создать администратора `python manage.py createsuperuser`.
4. Запустить сервер `python manage.py runserver` .