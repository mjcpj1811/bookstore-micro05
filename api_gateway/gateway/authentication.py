import jwt
from django.conf import settings
from rest_framework import authentication, exceptions


class JWTAuthentication(authentication.BaseAuthentication):
    """Simple JWT auth using the shared JWT_SECRET.

    Expects: Authorization: Bearer <token>
    Returns a lightweight user object built from token claims.
    """

    def authenticate(self, request):
        auth_header = request.headers.get('Authorization') or ''
        if not auth_header.startswith('Bearer '):
            return None

        token = auth_header.split(' ', 1)[1].strip()
        if not token:
            return None

        try:
            # Relax some validations (iat, sub) to avoid issues when
            # service clocks are slightly skewed or `sub` is numeric.
            # Signature and exp are still verified by default.
            payload = jwt.decode(
                token,
                settings.JWT_SECRET,
                algorithms=[getattr(settings, 'JWT_ALGORITHM', 'HS256')],
                options={"verify_iat": False, "verify_sub": False},
            )
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed('Invalid token')

        # Minimal user-like object with attributes from payload
        class AuthUser:
            def __init__(self, data):
                for k, v in data.items():
                    setattr(self, k, v)

            @property
            def is_authenticated(self):
                return True

        return AuthUser(payload), None
