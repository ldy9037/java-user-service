from django.test import TestCase
from certification.models import Certification
from datetime import datetime
import time
import random

class CertificationTest(TestCase):

    def test_certification_validation(self):
        cert_number = str(random.randrange(1, 1000000)).rjust(6, '0')
        unix_timestamp = int(time.mktime(datetime.now().timetuple()) * 1000)
  
        certification = Certification( 
            phone_number = "010-5264-5565",
            number = cert_number,
            ttl = unix_timestamp + (180 * 1000)
        )

        self.assertEqual(certification.phone_number, "010-5264-5565")
        self.assertEqual(certification.number, cert_number)
        self.assertEqual(certification.ttl, unix_timestamp + (180 * 1000))
        certification.full_clean()
        
            