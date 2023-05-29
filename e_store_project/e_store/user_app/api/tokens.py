import jwt
from datetime import datetime, timedelta
from django.conf import settings


def generate_tokens(user):
    """
    Generate access and refresh tokens for the given user.

    Parameters:
    - user: a User object representing the user for whom
            tokens are to be generated

    Returns:
    - A tuple containing the access token and refresh token

    """
    access_token_expiry = datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRY_MINUTES)
    refresh_token_expiry = datetime.utcnow() + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRY_DAYS)

    access_payload = {
        'user_id': user.id,
        'email': user.email,
        'exp': access_token_expiry,
        'type': 'access'
    }

    refresh_payload = {
        'user_id': user.id,
        'email': user.email,
        'exp': refresh_token_expiry,
        'type': 'refresh'
    }

    access_token = jwt.encode(
                            access_payload,
                            settings.SECRET_KEY,
                            algorithm='HS256'
                            )
    refresh_token = jwt.encode(
                            refresh_payload,
                            settings.SECRET_KEY,
                            algorithm='HS256'
                            )

    return access_token, refresh_token
