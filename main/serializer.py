from rest_framework import serializers
from .models import User


class RegisterUserSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=125)
    last_name = serializers.CharField(max_length=125)
    email = serializers.EmailField()
    username = serializers.CharField(max_length=125)
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    def validate_email(self, value):
         if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already registered.")
         return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username is already registered.")
        return value


class LoginSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)