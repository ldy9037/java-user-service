from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from certification.models import Certification
from user.models import User
from user_service import utils 
from argon2 import PasswordHasher

class CertificationTests(APITestCase):
    def test_request_cert_number(self):
        
        # 인증번호 요청에 대한 레코드가 잘 생성되었는지 검증하는 test code 
        # 아쉬운 점은 count 체크 대신 response에서 받은 id로 레코드를 찾아와서 assert하는 로직을 구현했으면 더 좋았을 것 같음.
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

        # 전달받은 인증번호로 patch 요청해 인증 완료 처리를 검증하는 test code
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
        # 휴대폰 중복체크 처리 검증을 위한 test code
        User.objects.create(
            email='ldy9037@naver.com', 
            name='이동열', 
            nickname='hani_6_6',
            phone_number='010-5264-5565',
            password=PasswordHasher().hash("!@#$12345d")
        )

        url = reverse('request-certification-number')
        data = {
            'phone_number': '010-5264-5565' 
         }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "이미 가입된 휴대폰 번호입니다.")