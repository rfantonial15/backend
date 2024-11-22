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

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "firstname",
            "lastname",
            "username",
            "email",
            "phone",
            "barangay",
            "password"
        ]
        extra_kwargs = {"password":{"write_only":True}}
    
    def create(self, validated_data):
        user = User.objects.create_user(
            firstname=validated_data["firstname"],
            lastname=validated_data["lastname"],
            username=validated_data["username"],
            email=validated_data["email"],
            phone=validated_data["phone"],
            barangay=validated_data["barangay"],
            password=validated_data["password"]
        )   
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)