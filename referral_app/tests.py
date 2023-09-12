from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase

from .utils import redis_auth_code
from .models import Profile


class ProfileTests(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('api/', include('referral_app.urls')),
    ]
    phone = '+79297845297'

    def test_login_create_profile(self, phone=phone):

        url = reverse('login_create')
        data = {'phone': phone}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_entry_by_code_profile(self, phone=phone):
        code_redis = redis_auth_code.get(phone)
        if code_redis:
            code_redis = code_redis.decode("utf-8")
        else:
            assert False

        url = reverse('entry_by_code')
        data = {'phone': phone,
                'authcode': code_redis}
        print(data)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual('token' in response.data, True)


