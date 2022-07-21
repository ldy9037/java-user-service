from django.db import models
from user_service import validators, utils

# 인증에 대한 model 
# 인증 유효기간/인증자 검증 부분이 아쉬움.
class Certification(models.Model):
    # 휴대폰 인증이기 때문에 null이면 안됨
    # validator로는 custom으로 생성한 휴대폰 번호 validator 사용 XXX-XXXX-XXXX 형식 검증
    phone_number = models.CharField(
        max_length=15,
        null=False,
        validators=[validators.validate_phone_number]
    )

    # 6자리 랜덤한 숫자를 생성해서 저장함.
    number = models.CharField(
        blank=True,
        max_length=6,
        default=utils.create_cert_number
    )

    # 기본값으로 현재 시간에서 3분을 더해서 저장 (timestamp)
    # 인증번호 체크 시 체크한 시간이 이 시간을 초과하면 인증이 안됨
    ttl = models.IntegerField(
        default=utils.create_timestamp_ttl(180)
    )

    # 인증되었는지 여부 True면 인증된 것
    certified = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        blank=True,
        auto_now_add=True
    )