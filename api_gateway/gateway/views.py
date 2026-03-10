import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class ProxyView(APIView):
    """
    Generic proxy view that forwards requests to microservices.
    """
    service_url = None
    service_path = ''

    def _proxy(self, request, path=''):
        url = f"{self.service_url}/{self.service_path}{path}"
        if request.query_params:
            url += '?' + request.query_params.urlencode()

        method = request.method.lower()
        kwargs = {'timeout': 10}

        if method in ('post', 'put', 'patch'):
            kwargs['json'] = request.data
        
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


class ManagerProxy(ProxyView):
    service_url = settings.SERVICE_URLS['MANAGER_SERVICE']
    service_path = 'api/manager/'


class CustomerProxy(ProxyView):
    service_url = settings.SERVICE_URLS['CUSTOMER_SERVICE']
    service_path = 'api/customers/'


class CatalogProxy(ProxyView):
    service_url = settings.SERVICE_URLS['CATALOG_SERVICE']
    service_path = 'api/catalog/'


class BookProxy(ProxyView):
    service_url = settings.SERVICE_URLS['BOOK_SERVICE']
    service_path = 'api/books/'


class CartProxy(ProxyView):
    service_url = settings.SERVICE_URLS['CART_SERVICE']
    service_path = 'api/carts/'


class OrderProxy(ProxyView):
    service_url = settings.SERVICE_URLS['ORDER_SERVICE']
    service_path = 'api/orders/'


class ShipProxy(ProxyView):
    service_url = settings.SERVICE_URLS['SHIP_SERVICE']
    service_path = 'api/shipments/'


class PayProxy(ProxyView):
    service_url = settings.SERVICE_URLS['PAY_SERVICE']
    service_path = 'api/payments/'


class ReviewProxy(ProxyView):
    service_url = settings.SERVICE_URLS['COMMENT_RATE_SERVICE']
    service_path = 'api/reviews/'


class RecommendationProxy(ProxyView):
    service_url = settings.SERVICE_URLS['RECOMMENDER_AI_SERVICE']
    service_path = 'api/recommendations/'


class ApiRootView(APIView):
    """API root listing all available endpoints."""
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
    def get(self, request):
        results = {}
        for name, url in settings.SERVICE_URLS.items():
            try:
                resp = requests.get(f"{url}/api/", timeout=3)
                results[name] = {'status': 'up', 'code': resp.status_code}
            except requests.RequestException:
                results[name] = {'status': 'down'}
        return Response(results)
