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