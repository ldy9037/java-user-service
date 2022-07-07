from dataclasses import field
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.UserSerializer):
    class Meta: 
        model = User
        fields = ('id', 'email', 'name')
