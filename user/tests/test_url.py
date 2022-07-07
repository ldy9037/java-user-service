from django.urls import reverse
from argon2 import PasswordHasher
from rest_framework import status
from rest_framework.test import APITestCase
from user.models import User

class UserTests(APITestCase):
    def test_create_user(self):
        
        url = reverse('list-insert-users')
        data = {
            'email': 'ldy9037@naver.com', 
            'name': '이동열', 
            'nickname': 'hani_6_6',
            'phone_number': '010-5264-5565',
            'password': PasswordHasher().hash("12345678")
         }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'ldy9037@naver.com')
        self.assertEqual(User.objects.get().name, '이동열')
        self.assertEqual(User.objects.get().nickname, 'hani_6_6')
        self.assertEqual(User.objects.get().phone_number, '010-5264-5565')
        self.assertTrue(PasswordHasher().verify(User.objects.get().password, "12345678"))
        
