import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from user_app.models import User, BlacklistedToken


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', None)
        
        if auth_header:
            token = auth_header.split()[1]
        else:
            raise AuthenticationFailed("Authentication header not specified")

        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY,
                algorithms=['HS256'],
                )
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except jwt.DecodeError:
            raise AuthenticationFailed('Token is invalid')

        token_type = payload['type']
        if token_type == 'access':
            if BlacklistedToken.objects.filter(token=token).exists():
                raise AuthenticationFailed('Token is invalid')
            user = User.objects.get(id=payload['user_id'])
            return (user, token)

        else:
            raise AuthenticationFailed("Invalid Token type")