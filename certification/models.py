from django.db import models
from user_service import validators

class Certification(models.Model):
    phone_number = models.CharField(
        max_length=15,
        unique=True,
        null=False,
        validators=[validators.validate_phone_number]
    )

    number = models.CharField(
        max_length=6,
        null=False
    )

    ttl = models.IntegerField(
        null=False
    )

    created_at = models.DateTimeField(
        null=False,
        auto_now_add=True
    )