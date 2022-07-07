from django.db import models
from .validators import validate_name

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