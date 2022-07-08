from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from certification.models import Certification
from user_service import utils 

class CertificationTests(APITestCase):
    def test_request_cert_number(self):
        
        url = reverse('request-certification-number')
        data = {
            'phone_number': '010-5264-5565' 
         }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.data['message'], "인증 번호가 전송되었습니다.")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Certification.objects.count(), 1)
        self.assertEqual(Certification.objects.get().phone_number, '010-5264-5565')
        self.assertTrue(Certification.objects.get().ttl > utils.create_timestamp_ttl(0))
        self.assertIsNotNone(Certification.objects.get().number)
        self.assertIsNotNone(Certification.objects.get().created_at)
