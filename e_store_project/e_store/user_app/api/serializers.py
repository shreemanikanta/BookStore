from rest_framework import serializers
from user_app.models import User, Role


class RolesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = '__all__'


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer class for user registration.
    """
    role = serializers.IntegerField(required=True)
    email = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = [
                    'username', 'first_name',
                    'last_name', 'email',
                    'password', 'role'
                ]
        extra_kwargs = {'password': {'write_only': True}}


class LoginSerializer(serializers.Serializer):
    """
    Serializer class for user login.
    """
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
