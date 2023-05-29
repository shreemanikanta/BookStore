from rest_framework.views import APIView
from rest_framework import status
from user_app.models import User, Role, BlacklistedToken
from user_app.api.serializers import (RegistrationSerializer,
                                      LoginSerializer, RolesSerializer)
from rest_framework.response import Response
from django.contrib.auth import authenticate
from book_store_app.api.authentication import JWTAuthentication
from user_app.api.tokens import generate_tokens
import jwt
from django.conf import settings
from django.db import IntegrityError
from django.http import JsonResponse


class RegistrationView(APIView):
    """
    View for creating a new user account.

    Methods:
        post(request): creates a new user account with the provided data.
    """
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(
                                    username=request.data.get('username'),
                                    email=request.data.get('email'),
                                    password=request.data.get('password'),
                                    first_name=request.data.get('first_name'),
                                    last_name=request.data.get('last_name')
                                    )
            role_id = request.data.get('role')
            role = Role.objects.get(id=role_id)
            user.user_roles.create(role=role)
            data = {
                'success': 'Account created successfully!',
                'user': serializer.data,
                'user_id': user.id
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        role = Role.objects.all()
        serializer = RolesSerializer(role, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LoginView(APIView):
    """
    View for handling user login requests.

     Methods:
        post(request): logs in the user with the provided username
                        and password.

    Returns:
        Response object with the user's tokens if login was successful,
        or an error message if the login failed.
    """
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = request.data.get('username')
            password = request.data.get('password')
            user = authenticate(username=username, password=password)
            if not user:
                return Response({'error': "Invalid username or password"},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                tokens = generate_tokens(user)
                access, refresh = tokens
            role = user.user_roles.get().role.role
            data = {
                'message': "logged in successfully",
                'username': user.username,
                'first_name': user.first_name,
                'role': role,
                'tokens': {'refresh': refresh, 'access': access}
            }
            return Response(data, status=status.HTTP_200_OK)

        else:
            return Response({'error': "Invalid username or password"},
                            status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """
    User logout and the JWT token was destroyed
    """
    authentication_classes = [JWTAuthentication]


    def post(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', None).split()[1]

        try:
            BlacklistedToken.objects.create(token=token)
            return JsonResponse({'message': 'Successfully logged out.'},
                                status=status.HTTP_200_OK)

        except IntegrityError:
            return JsonResponse({'error': 'Token has expired.'}, status=401)

        