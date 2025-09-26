from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db import IntegrityError
from .models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password],
        style={'input_type': 'password'},
        required=False,  # Password is optional for admin-created users
        allow_blank=True
    )
    password_confirm = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
        required=False,  # Password confirmation is optional
        allow_blank=True
    )

    class Meta:
        model = User
        fields = [
            'firstname', 'lastname', 'country_code', 'mobile_number',
            'email_address', 'password', 'password_confirm', 'role',
            'identification_number'
        ]

    def validate(self, attrs):
        if not attrs.get('mobile_number'):
            attrs['mobile_number'] = None  # Convert empty string to None
        
        # Validate password only if provided
        if attrs.get('password') or attrs.get('password_confirm'):
            if attrs.get('password') != attrs.get('password_confirm'):
                raise serializers.ValidationError({"password_confirm": "Passwords don't match."})
        
        # Validate role
        if attrs.get('role') not in ['landlord', 'tenant']:
            raise serializers.ValidationError({"role": "Role must be either 'landlord' or 'tenant'."})
        
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm', None)
        user = User.objects.create_user(**validated_data)
        return user

class SocialRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['firstname', 'lastname', 'email_address', 'provider', 'uid', 'photo_url', 'role']
        extra_kwargs = {
            'email_address': {'validators': []}  # Disable default uniqueness validation
        }

    def validate_email_address(self, value):
        provider = self.initial_data.get('provider')
        if provider == 'email' and User.objects.filter(email_address=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate(self, attrs):
        if attrs.get('role') not in ['landlord', 'tenant']:
            raise serializers.ValidationError({"role": "Role must be either 'landlord' or 'tenant'."})
        return attrs

    def create(self, validated_data):
        provider = validated_data.get('provider')
        email = validated_data.get('email_address')
        user = User.objects.filter(email_address=email).first()
        if user:
            if user.provider != provider:
                raise serializers.ValidationError(
                    f"User is registered with {user.provider.capitalize()}, not {provider.capitalize()}."
                )
            return user
        try:
            user = User.objects.create_user(
                **validated_data,
                provider=provider,
                is_active=True
            )
            user.verified_at = timezone.now()
            user.save()
            return user
        except IntegrityError:
            raise serializers.ValidationError("Failed to create user due to a conflict.")

class UserLoginSerializer(serializers.Serializer):
    email_address = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    is_verified = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = [
            'id', 'firstname', 'lastname', 'full_name', 'country_code',
            'mobile_number', 'email_address', 'is_verified', 'verified_at',
            'created_at', 'updated_at', 'role', 'identification_number'
        ]
        read_only_fields = ['id', 'verified_at', 'created_at', 'updated_at']

class UserListSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = [
            'id', 'firstname', 'lastname', 'full_name', 'email_address',
            'mobile_number', 'role', 'identification_number', 'is_active'
        ]

class AccountVerificationSerializer(serializers.Serializer):
    email_address = serializers.EmailField()
    verification_code = serializers.CharField(max_length=10)

class PasswordResetRequestSerializer(serializers.Serializer):
    email_address = serializers.EmailField()

class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=64)
    new_password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
        required=True
    )
    password_confirm = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
        required=True
    )

    def validate_new_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value

    def validate(self, attrs):
        if attrs['new_password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password_confirm": "Passwords don't match"})
        return attrs