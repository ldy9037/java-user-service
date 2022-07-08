from django.db import models
from user_service.validators import validate_name, validate_phone_number

class User(models.Model):
    email = models.EmailField(
        max_length=254, 
        unique=True, 
        null=False
        )

    name = models.CharField(
        max_length=30, 
        null=False,
        validators=[validate_name]
    )

    nickname = models.CharField(
        max_length=30,
        unique=True,
        null=False
    )

    phone_number = models.CharField(
        max_length=15,
        unique=True,
        null=False,
        validators=[validate_phone_number]
    )

    password = models.CharField(
        max_length=254,
        null=False
    )

    
