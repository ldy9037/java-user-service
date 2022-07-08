from django.db import models
from user_service import validators, utils

class Certification(models.Model):
    phone_number = models.CharField(
        max_length=15,
        null=False,
        validators=[validators.validate_phone_number]
    )

    number = models.CharField(
        blank=True,
        max_length=6,
        default=utils.create_cert_number
    )

    ttl = models.IntegerField(
        default=utils.create_timestamp_ttl(180)
    )

    certified = models.IntegerField(
        default=0
    )

    created_at = models.DateTimeField(
        blank=True,
        auto_now_add=True
    )