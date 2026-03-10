import requests
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from .models import Customer, ShippingAddress
from .serializers import CustomerSerializer, ShippingAddressSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def create(self, request, *args, **kwargs):
        """Register customer and auto-create cart via cart-service."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        customer = serializer.save()

        # Auto-create cart in cart-service
        try:
            requests.post(
                f"{settings.SERVICE_URLS['CART_SERVICE']}/api/carts/",
                json={'customer_id': customer.id},
                timeout=5,
            )
        except requests.RequestException:
            pass  # Cart creation failure is non-blocking

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['post'])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            customer = Customer.objects.get(username=username, is_active=True)
        except Customer.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        if not check_password(password, customer.password):
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(CustomerSerializer(customer).data)

    @action(detail=True, methods=['get'])
    def addresses(self, request, pk=None):
        customer = self.get_object()
        addrs = ShippingAddress.objects.filter(customer=customer)
        return Response(ShippingAddressSerializer(addrs, many=True).data)


class ShippingAddressViewSet(viewsets.ModelViewSet):
    queryset = ShippingAddress.objects.all()
    serializer_class = ShippingAddressSerializer

    def get_queryset(self):
        customer_id = self.request.query_params.get('customer_id')
        if customer_id:
            return ShippingAddress.objects.filter(customer_id=customer_id)
        return ShippingAddress.objects.all()

    @action(detail=True, methods=['post'])
    def set_default(self, request, pk=None):
        addr = self.get_object()
        ShippingAddress.objects.filter(customer=addr.customer).update(is_default=False)
        addr.is_default = True
        addr.save()
        return Response({'status': 'default address set'})
