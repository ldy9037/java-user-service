from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from user.models import User

class UserTests(APITestCase):
    def test_create_user(self):
        
        url = reverse('list-insert-users')
        data = {'email': 'ldy9037@naver.com', 'name': '이동열', 'nickname': 'hani_6_6'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().name, '이동열')
