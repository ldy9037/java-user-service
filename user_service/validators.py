from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re

def validate_name(value):
    pattern = re.compile(r'^[a-zA-Z가-힣]*$')

    if not pattern.match(str(value)):
        raise ValidationError(
            _('%(value)는 이름 형식이 아닙니다.'),
            params={'value': value},
        )

def validate_phone_number(value):
    pattern = re.compile(r'^01([0-9])-([0-9]{3,4})-([0-9]{4})$')

    if not pattern.match(str(value)):
        raise ValidationError(
            _('%(value)는 휴대폰 번호 형식이 아닙니다.'),
            params={'value': value},
        )

def validate_password(value):
    # 8자 ~ 20자/영문자/숫자가 각각 하나 이상씩 포함되어 있어야 함.
    pattern = re.compile(r'^(?=.*\d)(?=.*[a-zA-Z])[0-9a-zA-Z!@#$%^&*]{8,20}$')

    if not pattern.match(str(value)):
        raise ValidationError(
            _('올바른 비밀번호 형식이 아닙니다.(8-20자/영문자/숫자 한개 이상)')
        )