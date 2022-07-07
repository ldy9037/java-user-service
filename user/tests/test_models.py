from django.core.exceptions import ValidationError
from django.test import TestCase
import re

from user.models import User


class UserTest(TestCase):

    def test_name_contains_special_characters(self):
        user = User( email = "ldy9037@naver.com", name = "이동열")
        user.full_clean()

        with self.assertRaises(ValidationError):
            user.name = "이동열!"
            user.full_clean()

        
            