from rest_framework import serializers
from .models import Certification

class CertificationSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Certification
        fields = ('id', 'number', 'phone_number')