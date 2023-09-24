from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.hashers import make_password

from . import models

class SignupSerializer(serializers.ModelSerializer):

    confirm_password = serializers.CharField(
        max_length=100,
        required=True,
        allow_blank=False,
        trim_whitespace=True,
        help_text="Confirm Password."
    )

    class Meta:
        model = models.User
        fields = [
            'full_name',
            'email',
            'contact',
            'password',

        ]

        extra_kwargs = {
            'full_name': {'required': True},
            'email': {'required': True},
            'contact': {'required': True},
            'password': {'required': True},
        }

        def validate(self, data):
            password = data.get('password')
            password2 = data.get('confirm_password')

            if password != password2:
                raise ValidationError("Passwords do not match.")
            
            data['password'] = make_password(password2)

            return data
        

    
class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField(
        required = True,
        help_text="Enter Email."
    )

    password = serializers.CharField(
        max_length=100,
        required=True,
        allow_blank=False,
        trim_whitespace=True,
        help_text="Password"
    )

        

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fileds = [
            "email",
            "org",
            "contact",
            "is_staff",
            "is_active",
            "is_superuser",
        ]



class ForgotPasswordSerializer(serializers.Serializer):

    email = serializers.EmailField(
        required=False,
        help_text="Email"
    )
    
class NewPasswordSerializer(serializers.Serializer):

    password1 = serializers.CharField(max_length = 255, required =True)
    password2 = serializers.CharField(max_length = 255, required =True)

    def validate(self, data):
        # Check if the passwords match
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("The passwords do not match.")
        
        if len(data['password1']) < 6:
            raise serializers.ValidationError("Your Password is very weak")
        
        return data