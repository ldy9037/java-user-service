from django.db import models
from user_service.validators import validate_name, validate_phone_number
from django.contrib.auth.models import AbstractBaseUser

class User(AbstractBaseUser):
    email = models.EmailField(
        max_length=254, 
        unique=True, 
        null=False
        )

    # 한글과 영어만 가능하도록 custom 유효성 검증기 추가
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

    # save() 메서드를 override해서 암호화 후 저장되게 했어도 괜찮았을 듯
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
    

    
