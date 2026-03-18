import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny


class ProxyView(APIView):
    """
    Generic proxy view that forwards requests to microservices.
    """
    service_url = None
    service_path = ''
    # None = no role restriction, list = allowed roles from JWT token
    required_roles = None

    # Mặc định cho phép, chỉ chặn bằng _check_role khi có token và role không phù hợp.
    permission_classes = [AllowAny]

    def _check_role(self, request):
        # Nếu không cấu hình required_roles thì không kiểm tra.
        if self.required_roles is None:
            return

        # Với endpoint có required_roles thì bắt buộc phải có JWT.
        auth_header = request.headers.get('Authorization') or ''
        if not auth_header.startswith('Bearer '):
            return Response({'detail': 'Authentication credentials were not provided'}, status=status.HTTP_401_UNAUTHORIZED)

        user = getattr(request, 'user', None)
        role = getattr(user, 'role', None) if user else None
        if role not in self.required_roles:
            return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

    def _proxy(self, request, path=''):
        role_error = self._check_role(request)
        if role_error is not None:
            return role_error

        url = f"{self.service_url}/{self.service_path}{path}"
        if request.query_params:
            url += '?' + request.query_params.urlencode()

        method = request.method.lower()
        kwargs = {'timeout': 10}

        if method in ('post', 'put', 'patch'):
            kwargs['json'] = request.data
        
        # Forward Authorization header if present so downstream services
        # can also inspect the JWT if needed.
        auth_header = request.headers.get('Authorization')
        if auth_header:
            kwargs.setdefault('headers', {})['Authorization'] = auth_header

        try:
            resp = getattr(requests, method)(url, **kwargs)
            return Response(resp.json(), status=resp.status_code)
        except requests.exceptions.ConnectionError:
            return Response(
                {'error': 'Service unavailable'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        except ValueError:
            return Response(
                {'detail': resp.text},
                status=resp.status_code,
            )

    def get(self, request, path=''):
        return self._proxy(request, path)

    def post(self, request, path=''):
        return self._proxy(request, path)

    def put(self, request, path=''):
        return self._proxy(request, path)

    def patch(self, request, path=''):
        return self._proxy(request, path)

    def delete(self, request, path=''):
        return self._proxy(request, path)


# --- Proxy classes for each service ---

class StaffProxy(ProxyView):
    service_url = settings.SERVICE_URLS['STAFF_SERVICE']
    service_path = 'api/staff/'
    required_roles = ['staff', 'manager']


class ManagerProxy(ProxyView):
    service_url = settings.SERVICE_URLS['MANAGER_SERVICE']
    service_path = 'api/manager/'
    required_roles = ['manager']


class CustomerProxy(ProxyView):
    service_url = settings.SERVICE_URLS['CUSTOMER_SERVICE']
    service_path = 'api/customers/'
    # Customer APIs stay publicly accessible; individual services
    # can enforce additional checks if needed.
    permission_classes = [AllowAny]


class CatalogProxy(ProxyView):
    service_url = settings.SERVICE_URLS['CATALOG_SERVICE']
    service_path = 'api/catalog/'
    permission_classes = [AllowAny]


class BookProxy(ProxyView):
    service_url = settings.SERVICE_URLS['BOOK_SERVICE']
    service_path = 'api/books/'
    permission_classes = [AllowAny]


class CartProxy(ProxyView):
    service_url = settings.SERVICE_URLS['CART_SERVICE']
    service_path = 'api/carts/'
    required_roles = ['customer']


class OrderProxy(ProxyView):
    service_url = settings.SERVICE_URLS['ORDER_SERVICE']
    service_path = 'api/orders/'
    required_roles = ['customer', 'staff', 'manager']


class ShipProxy(ProxyView):
    service_url = settings.SERVICE_URLS['SHIP_SERVICE']
    service_path = 'api/shipments/'
    required_roles = ['staff', 'manager']


class PayProxy(ProxyView):
    service_url = settings.SERVICE_URLS['PAY_SERVICE']
    service_path = 'api/payments/'
    required_roles = ['customer', 'manager']


class ReviewProxy(ProxyView):
    service_url = settings.SERVICE_URLS['COMMENT_RATE_SERVICE']
    service_path = 'api/reviews/'
    required_roles = ['customer']


class RecommendationProxy(ProxyView):
    service_url = settings.SERVICE_URLS['RECOMMENDER_AI_SERVICE']
    service_path = 'api/recommendations/'
    required_roles = ['customer']


class AuthProxy(ProxyView):
    """Proxy to auth-service for login and other auth endpoints."""

    service_url = settings.SERVICE_URLS['AUTH_SERVICE']
    service_path = 'api/auth/'
    # Auth endpoints không cần JWT; luôn cho phép để user có thể
    # đăng nhập lại kể cả khi token cũ đã hết hạn/không hợp lệ.
    permission_classes = [AllowAny]
    authentication_classes = []


class ApiRootView(APIView):
    """API root listing all available endpoints."""
    permission_classes = [AllowAny]
    def get(self, request):
        base = request.build_absolute_uri('/api/')
        return Response({
            'health': base + 'health/',
            'staff': base + 'staff/',
            'manager': base + 'manager/',
            'customers': base + 'customers/',
            'catalog': base + 'catalog/',
            'books': base + 'books/',
            'carts': base + 'carts/',
            'orders': base + 'orders/',
            'shipments': base + 'shipments/',
            'payments': base + 'payments/',
            'reviews': base + 'reviews/',
            'recommendations': base + 'recommendations/',
        })


class ServiceHealthView(APIView):
    """Check health of all microservices."""
    permission_classes = [AllowAny]
    def get(self, request):
        results = {}
        for name, url in settings.SERVICE_URLS.items():
            try:
                resp = requests.get(f"{url}/api/", timeout=3)
                results[name] = {'status': 'up', 'code': resp.status_code}
            except requests.RequestException:
                results[name] = {'status': 'down'}
        return Response(results)
