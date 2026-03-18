import datetime

import jwt
import requests
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class LoginView(APIView):
    """Authenticate against user services and issue JWT."""

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Try each role-specific service in order: manager, staff, then customer
        candidates = [
            ('manager', settings.SERVICE_URLS['MANAGER_SERVICE'], 'api/manager/login/'),
            ('staff', settings.SERVICE_URLS['STAFF_SERVICE'], 'api/staff/login/'),
            ('customer', settings.SERVICE_URLS['CUSTOMER_SERVICE'], 'api/customers/login/'),
        ]

        user_data = None
        user_role = None

        for role, base_url, path in candidates:
            try:
                resp = requests.post(
                    f"{base_url}/{path}",
                    json={'username': username, 'password': password},
                    timeout=5,
                )
            except requests.RequestException:
                continue

            if resp.status_code == 200:
                try:
                    user_data = resp.json()
                except ValueError:
                    user_data = None
                if user_data:
                    user_role = role
                    break

        if not user_data or not user_role:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        payload = {
            'sub': user_data.get('id'),
            'username': user_data.get('username'),
            'role': user_role,
            'iat': int(datetime.datetime.utcnow().timestamp()),
            'exp': int((datetime.datetime.utcnow() + datetime.timedelta(seconds=settings.JWT_EXP_SECONDS)).timestamp()),
        }

        token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

        return Response({
            'token': token,
            'user': user_data,
            'role': user_role,
        })
