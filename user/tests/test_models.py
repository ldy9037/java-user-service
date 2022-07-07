from django.core.exceptions import ValidationError
from django.test import TestCase
import re

from user.models import User


class UserTest(TestCase):

    def test_user_validation(self):
        user = User( email = "ldy9037@naver.com", name = "이동열", nickname="hani_6_6")
        self.assertEqual(user.email, "ldy9037@naver.com")
        self.assertEqual(user.name, "이동열")
        self.assertEqual(user.nickname, "hani_6_6")
        user.full_clean()

        with self.assertRaises(ValidationError):
            user.name = "이동열!"
            user.full_clean()

            
            