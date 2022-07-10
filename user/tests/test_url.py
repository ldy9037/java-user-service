from http import client
from django.urls import reverse
from argon2 import PasswordHasher
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from user.models import User
from certification.models import Certification

class UserTests(APITestCase):
    def test_create_user(self):
        certification = Certification.objects.create(
            phone_number = '010-5264-5565',
            certified = True
        )

        url = reverse('insert-users')
        data = {
            'email': 'ldy9037@naver.com', 
            'name': '이동열', 
            'nickname': 'hani_6_6',
            'phone_number': '010-5264-5565',
            'plain_password': "!@#ldy12345",
            'cert_id': certification.id
         }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'ldy9037@naver.com')
        self.assertEqual(User.objects.get().name, '이동열')
        self.assertEqual(User.objects.get().nickname, 'hani_6_6')
        self.assertEqual(User.objects.get().phone_number, '010-5264-5565')
        self.assertTrue(PasswordHasher().verify(User.objects.get().password, "!@#ldy12345"))

    def test_count_users(self):
        User.objects.create(
            email = 'ldy9037@naver.com', 
            name = '이동열', 
            nickname = 'hani_6_6',
            phone_number = '010-5264-5565',
            password = PasswordHasher().hash("12345678")
        )

        url = reverse('count-users', kwargs={'value': 'ldy9037@naver.com'})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 1)
        self.assertEqual(response.data['phone_number'], 0)

    def test_get_user(self):
        User.objects.create(
            email = 'ldy9037@naver.com', 
            name = '이동열', 
            nickname = 'hani_6_6',
            phone_number = '010-5264-5565',
            password = PasswordHasher().hash("12345678")
        )

        url = reverse('token-obtain-pair')
        data = {
            'email': 'ldy9037@naver.com',
            'password': '12345678'
         }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer '+response.data['access'])
       
        url = reverse('get-users', kwargs={'id': User.objects.get().id})

        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['id'], User.objects.get().id)
        self.assertEqual(response.data['user']['email'], 'ldy9037@naver.com')
        self.assertEqual(response.data['user']['name'], '이동열')
        self.assertEqual(response.data['user']['nickname'], 'hani_6_6')
        self.assertEqual(response.data['user']['phone_number'], '010-5264-5565')

    def test_find_password(self):
        certification = Certification.objects.create(
            phone_number = '010-5264-5565',
            certified = True
        )

        url = reverse('find-password')
        data = {
            'phone_number': '010-5264-5565',
            'plain_password': "!@#ldy12345",
            'cert_id': certification.id
         }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)