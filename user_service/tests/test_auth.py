from django.urls import reverse
from argon2 import PasswordHasher
from rest_framework import status
from rest_framework.test import APITestCase
from user.models import User

class AuthTests(APITestCase):
    def test_login(self):
        user = User.objects.create(
            email='ldy9037@naver.com',
            name='이동열',
            nickname='hani_6_6',
            phone_number='010-5264-5565',
            password=PasswordHasher().hash("!@#qwe123")
        )

        url = reverse('token-obtain-pair')
        data = {
            'email': 'ldy9037@naver.com',
            'password': '!@#qwe123'
         }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)