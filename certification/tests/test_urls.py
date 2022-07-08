from django.urls import reverse
import certification
from rest_framework import status
from rest_framework.test import APITestCase
from certification.models import Certification
from user.models import User
from user_service import utils 

class CertificationTests(APITestCase):
    def test_request_cert_number(self):
        
        url = reverse('request-certification-number')
        data = {
            'phone_number': '010-5264-5565' 
         }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Certification.objects.count(), 1)
        self.assertEqual(Certification.objects.get().phone_number, '010-5264-5565')
        self.assertTrue(Certification.objects.get().ttl > utils.create_timestamp_ttl(0))
        self.assertIsNotNone(Certification.objects.get().number)
        self.assertIsNotNone(Certification.objects.get().created_at)

        data = {
            'id': response.data['cert_id'],
            'phone_number' : '010-5264-5565',
            'number' : Certification.objects.get().number
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['cert_id'], data['id'])
        self.assertEqual(response.data['phone_number'], data['phone_number'])

        certification = Certification.objects.filter(id=response.data['cert_id'])
        self.assertTrue(certification.get().certified)

    def test_phone_number_already_exists(self):
        url = reverse('list-insert-users')
        data = {
            'email': 'ldy9037@naver.com', 
            'name': '이동열', 
            'nickname': 'hani_6_6',
            'phone_number': '010-5264-5565',
            'password': "12345678"
         }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('request-certification-number')
        data = {
            'phone_number': '010-5264-5565' 
         }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "이미 가입된 휴대폰 번호입니다.")