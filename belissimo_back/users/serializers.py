from  rest_framework import serializers
from .models import User,TenantAssignment,


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'role', 'phone_number',
            'government_id', 'dob', 'email', 'password'
        ]
        read_only_fields = ['id']
        extra_kwargs = {
            'email': {'required': True},
            'password': {'write_only': True, 'required': False},
        }
