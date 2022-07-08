from django.test import TestCase
from certification.models import Certification
from user_service import utils

class CertificationTest(TestCase):

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
        
            