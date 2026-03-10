from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import PaymentMethod, Payment
from .serializers import PaymentMethodSerializer, PaymentSerializer


class PaymentMethodViewSet(viewsets.ModelViewSet):
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def get_queryset(self):
        qs = Payment.objects.select_related('payment_method')
        order_id = self.request.query_params.get('order_id')
        if order_id:
            qs = qs.filter(order_id=order_id)
        customer_id = self.request.query_params.get('customer_id')
        if customer_id:
            qs = qs.filter(customer_id=customer_id)
        return qs

    def create(self, request, *args, **kwargs):
        """Create payment. Auto-assign payment method by code or ID."""
        data = request.data.copy()
        method_val = data.pop('payment_method', None)
        if isinstance(method_val, str):
            try:
                method = PaymentMethod.objects.get(code=method_val, is_active=True)
                data['payment_method'] = method.id
            except PaymentMethod.DoesNotExist:
                data['payment_method'] = None
        elif method_val is not None:
            data['payment_method'] = method_val
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        payment = self.get_object()
        transaction_id = request.data.get('transaction_id', '')
        payment.status = 'completed'
        payment.transaction_id = transaction_id
        from django.utils import timezone
        payment.confirmed_at = timezone.now()
        payment.save()
        return Response(PaymentSerializer(payment).data)

    @action(detail=True, methods=['post'])
    def refund(self, request, pk=None):
        payment = self.get_object()
        payment.status = 'refunded'
        payment.save()
        return Response(PaymentSerializer(payment).data)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        payment = self.get_object()
        payment.status = 'cancelled'
        payment.failure_reason = request.data.get('reason', 'Cancelled by user')
        payment.save()
        return Response(PaymentSerializer(payment).data)
