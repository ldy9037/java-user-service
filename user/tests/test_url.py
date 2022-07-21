from http import client
from django.urls import reverse
from argon2 import PasswordHasher
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from user.models import User
from certification.models import Certification

class UserTests(APITestCase):
    # user 생성에 대한 테스트
    def test_create_user(self):
        # 휴대폰 인증 처리를 위해 certification record를 미리 한개 생성
        certification = Certification.objects.create(
            phone_number = '010-5264-5565',
            certified = True
        )

        url = reverse('insert-users')
        # 인증 정보(id)와 함께 회원가입 요청
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
        # 이 부분도 get으로 그냥 가져오는 대신 id 검색해서 reponse와 비교했으면 좋았을 것 같음.
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'ldy9037@naver.com')
        self.assertEqual(User.objects.get().name, '이동열')
        self.assertEqual(User.objects.get().nickname, 'hani_6_6')
        self.assertEqual(User.objects.get().phone_number, '010-5264-5565')
        self.assertTrue(PasswordHasher().verify(User.objects.get().password, "!@#ldy12345"))

    def test_count_users(self):
        # 중복확인 view 테스트
        # 중복확인 검증 방식에 문제가 없을지? 
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
        # 내 정보 가져오기 test
        User.objects.create(
            email = 'ldy9037@naver.com', 
            name = '이동열', 
            nickname = 'hani_6_6',
            phone_number = '010-5264-5565',
            password = PasswordHasher().hash("12345678")
        )

        # 먼저 로그인 (JWT Token 발급)
        # Token Claim 검증을 할 수 있었다면 좋았겠음. (base64 decode)
        url = reverse('token-obtain-pair')
        data = {
            'email': 'ldy9037@naver.com',
            'password': '12345678'
         }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 내 정보 요청은 인증된 사용자만이 요청할 수 있기 때문에 APIClient 객체를 생성해서 credentials에 HTTP_AUTHORIZATION 지정
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer '+response.data['access'])
       
        url = reverse('get-users', kwargs={'id': User.objects.get().id})

        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # get 대신 위에서 저장할 때 사용한 객체와 비교했으면 좋았을 듯
        self.assertEqual(response.data['user']['id'], User.objects.get().id)
        self.assertEqual(response.data['user']['email'], 'ldy9037@naver.com')
        self.assertEqual(response.data['user']['name'], '이동열')
        self.assertEqual(response.data['user']['nickname'], 'hani_6_6')
        self.assertEqual(response.data['user']['phone_number'], '010-5264-5565')

    def test_find_password(self):
        # 비밀번호 찾기 test
        # 비밀번호 찾기에는 휴대폰번호 인증이 필요하기 때문에 인증 record 생성
        certification = Certification.objects.create(
            phone_number = '010-5264-5565',
            certified = True
        )

        # 인증 정보와 함께 변경할 비밀번호 전달
        # 변경된 비밀번호로 로그인이 되는지 확인해봤으면 좋았을 것 같음
        url = reverse('find-password')
        data = {
            'phone_number': '010-5264-5565',
            'plain_password': "!@#ldy12345",
            'cert_id': certification.id
         }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)