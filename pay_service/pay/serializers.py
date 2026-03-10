from rest_framework import serializers
from .models import PaymentMethod, Payment


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    method_name = serializers.CharField(source='payment_method.name', read_only=True, default=None)
    payment_number = serializers.CharField(required=False)

    class Meta:
        model = Payment
        fields = '__all__'
