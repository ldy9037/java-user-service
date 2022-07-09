from itertools import count
from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from user.models import User
from django.db.models import Q
from argon2 import PasswordHasher

class Backend(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        user = User.objects.filter(Q(email=email) | Q(phone_number=email))

        if user.count() and PasswordHasher().verify(user.get().password, password):
            return user.get()
        
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None