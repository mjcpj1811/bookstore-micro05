from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Carrier, ShippingZone, ShippingRate, Shipment
from .serializers import CarrierSerializer, ShippingZoneSerializer, ShippingRateSerializer, ShipmentSerializer


class CarrierViewSet(viewsets.ModelViewSet):
    queryset = Carrier.objects.all()
    serializer_class = CarrierSerializer


class ShippingZoneViewSet(viewsets.ModelViewSet):
    queryset = ShippingZone.objects.all()
    serializer_class = ShippingZoneSerializer


class ShippingRateViewSet(viewsets.ModelViewSet):
    queryset = ShippingRate.objects.all()
    serializer_class = ShippingRateSerializer


class ShipmentViewSet(viewsets.ModelViewSet):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer

    def get_queryset(self):
        qs = Shipment.objects.select_related('carrier')
        order_id = self.request.query_params.get('order_id')
        if order_id:
            qs = qs.filter(order_id=order_id)
        customer_id = self.request.query_params.get('customer_id')
        if customer_id:
            qs = qs.filter(customer_id=customer_id)
        return qs

    def create(self, request, *args, **kwargs):
        """Create shipment, auto-assign carrier by code."""
        data = request.data.copy()
        carrier_code = data.pop('carrier_code', None)
        if carrier_code:
            try:
                carrier = Carrier.objects.get(code=carrier_code, is_active=True)
                data['carrier'] = carrier.id
            except Carrier.DoesNotExist:
                pass
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        shipment = self.get_object()
        new_status = request.data.get('status')
        if new_status not in dict(Shipment.STATUS_CHOICES):
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        shipment.status = new_status
        if new_status == 'delivered':
            from django.utils import timezone
            shipment.delivery_date = timezone.now()
        shipment.save()
        return Response(ShipmentSerializer(shipment).data)

    @action(detail=True, methods=['post'])
    def track(self, request, pk=None):
        shipment = self.get_object()
        tracking = request.data.get('tracking_number')
        if tracking:
            shipment.tracking_number = tracking
            shipment.save()
        return Response(ShipmentSerializer(shipment).data)
