from django.db import models
from user_service.validators import validate_name, validate_phone_number
from django.contrib.auth.models import AbstractBaseUser

class User(AbstractBaseUser):
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

    is_active = models.BooleanField(
        default=True
    )

    is_admin = models.BooleanField(
        default=False
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number', 'name']
    

    
