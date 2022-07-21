from itertools import count
from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from user.models import User
from django.db.models import Q
from argon2 import PasswordHasher

# 여러 문제가 있음. 일단 기본적으로 django의 user객체는 다중 username을 지원하지 않기 때문에 일반적인 방법으로는 email과 password 두 가지 방법으로 인증하는 방법이 존재하지 않음.
# 그래서 아래처럼
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