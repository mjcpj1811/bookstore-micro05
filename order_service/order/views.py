import requests
from decimal import Decimal
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Order, OrderItem, OrderStatusHistory
from .serializers import OrderSerializer, OrderItemSerializer, OrderStatusHistorySerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related('items', 'status_history')
    serializer_class = OrderSerializer

    def get_queryset(self):
        qs = Order.objects.prefetch_related('items', 'status_history')
        customer_id = self.request.query_params.get('customer_id')
        if customer_id:
            qs = qs.filter(customer_id=customer_id)
        order_status = self.request.query_params.get('status')
        if order_status:
            qs = qs.filter(status=order_status)
        return qs

    @action(detail=False, methods=['post'])
    def checkout(self, request):
        """
        Create order from cart. Triggers payment and shipping.
        Required: customer_id, shipping_address_id, payment_method, carrier_code
        """
        customer_id = request.data.get('customer_id')
        shipping_address_id = request.data.get('shipping_address_id')
        payment_method = request.data.get('payment_method', 'cod')
        carrier_code = request.data.get('carrier_code', 'standard')

        if not customer_id:
            return Response({'error': 'customer_id required'}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch cart from cart-service
        try:
            resp = requests.get(
                f"{settings.SERVICE_URLS['CART_SERVICE']}/api/carts/my_cart/",
                params={'customer_id': customer_id},
                timeout=5,
            )
            if resp.status_code != 200:
                return Response({'error': 'Could not fetch cart'}, status=status.HTTP_400_BAD_REQUEST)
            cart_data = resp.json()
        except requests.RequestException:
            return Response({'error': 'Cart service unavailable'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        cart_items = cart_data.get('items', [])
        if not cart_items:
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        # Calculate totals
        subtotal = sum(
            Decimal(str(item['price'])) * item['quantity']
            for item in cart_items
        )
        shipping_fee = Decimal('0.00')
        tax = Decimal('0.00')
        discount = Decimal('0.00')
        final_amount = subtotal + shipping_fee + tax - discount

        # Create order
        order = Order.objects.create(
            customer_id=customer_id,
            shipping_address_id=shipping_address_id,
            subtotal=subtotal,
            shipping_fee=shipping_fee,
            tax=tax,
            discount=discount,
            final_amount=final_amount,
            payment_method=payment_method,
            carrier_code=carrier_code,
        )

        # Create order items
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                book_id=item['book_id'],
                book_title=item.get('book_title', ''),
                quantity=item['quantity'],
                unit_price=item['price'],
                subtotal=Decimal(str(item['price'])) * item['quantity'],
            )

        OrderStatusHistory.objects.create(order=order, status='pending', description='Order created')

        # Trigger payment via pay-service
        try:
            requests.post(
                f"{settings.SERVICE_URLS['PAY_SERVICE']}/api/payments/",
                json={
                    'order_id': order.id,
                    'order_number': order.order_number,
                    'amount': str(final_amount),
                    'payment_method': payment_method,
                    'customer_id': customer_id,
                },
                timeout=5,
            )
        except requests.RequestException:
            pass

        # Trigger shipment via ship-service
        try:
            requests.post(
                f"{settings.SERVICE_URLS['SHIP_SERVICE']}/api/shipments/",
                json={
                    'order_id': order.id,
                    'order_number': order.order_number,
                    'carrier_code': carrier_code,
                    'customer_id': customer_id,
                    'shipping_address_id': shipping_address_id,
                    'shipping_cost': str(shipping_fee),
                },
                timeout=5,
            )
        except requests.RequestException:
            pass

        # Clear cart after successful order
        try:
            cart_id = cart_data.get('id')
            if cart_id:
                requests.post(
                    f"{settings.SERVICE_URLS['CART_SERVICE']}/api/carts/{cart_id}/clear/",
                    timeout=5,
                )
        except requests.RequestException:
            pass

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        order = self.get_object()
        new_status = request.data.get('status')
        description = request.data.get('description', '')
        changed_by = request.data.get('changed_by')

        if new_status not in dict(Order.STATUS_CHOICES):
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

        order.status = new_status
        if new_status == 'cancelled':
            from django.utils import timezone
            order.cancel_reason = request.data.get('cancel_reason', '')
            order.cancelled_at = timezone.now()
        order.save()

        OrderStatusHistory.objects.create(
            order=order,
            status=new_status,
            description=description,
            changed_by=changed_by,
        )
        return Response(OrderSerializer(order).data)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        from django.db.models import Count, Sum
        stats = Order.objects.values('status').annotate(
            count=Count('id'),
            total_amount=Sum('final_amount'),
        )
        return Response(list(stats))
