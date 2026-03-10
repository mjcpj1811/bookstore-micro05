from rest_framework import serializers
from .models import Carrier, ShippingZone, ShippingRate, Shipment


class CarrierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carrier
        fields = '__all__'


class ShippingZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingZone
        fields = '__all__'


class ShippingRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingRate
        fields = '__all__'


class ShipmentSerializer(serializers.ModelSerializer):
    carrier_name = serializers.CharField(source='carrier.name', read_only=True, default=None)
    shipment_number = serializers.CharField(required=False)

    class Meta:
        model = Shipment
        fields = '__all__'
