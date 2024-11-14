from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'firstname', 'lastname', 'email', 'username', 
            'phone', 'barangay', 'isadmin', 'is_verified'
        ]
        extra_kwargs = {
            'password': {'write_only': True},  # Ensure password is write-only
        }
