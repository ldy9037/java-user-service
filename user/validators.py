from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re

def validate_name(value):
    pattern = re.compile("[a-zA-Z가-힣]")

    if pattern.match(str(value)):
        raise ValidationError(
            _('%(value)는 이름 형식이 아닙니다.'),
            params={'value': value},
        )
