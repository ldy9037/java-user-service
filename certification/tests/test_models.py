from django.test import TestCase
from certification.models import Certification
from user_service import utils

class CertificationTest(TestCase):
    
    # Certification Model의 유효성 검증 동작을 확인하기 위해 작성하였음.
    # 하지만 Model을 테스트 하는 대신 serializer에 대한 테스트를 작성했으면 훨씬 검증이 쉬웠을 듯 함.
    def test_certification_validation(self):
        cert_number = utils.create_cert_number()
        ttl = utils.create_timestamp_ttl(180)
  
        certification = Certification( 
            phone_number = "010-5264-5565",
            number = cert_number,
            ttl = ttl
        )

        self.assertEqual(certification.phone_number, "010-5264-5565")
        self.assertEqual(certification.number, cert_number)
        self.assertEqual(certification.ttl, ttl)
        certification.full_clean()
        
            