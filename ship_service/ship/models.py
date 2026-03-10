from django.db import models
from django.utils import timezone
import uuid


class Carrier(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    website = models.URLField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    logo_url = models.URLField(max_length=500, blank=True, null=True)

    class Meta:
        db_table = 'carrier'

    def __str__(self):
        return self.name


class ShippingZone(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    countries = models.JSONField(blank=True, null=True)
    provinces = models.JSONField(blank=True, null=True)
    cities = models.JSONField(blank=True, null=True)

    class Meta:
        db_table = 'shipping_zone'

    def __str__(self):
        return self.name


class ShippingRate(models.Model):
    carrier = models.ForeignKey(Carrier, on_delete=models.CASCADE, related_name='rates')
    shipping_zone = models.ForeignKey(ShippingZone, on_delete=models.CASCADE, related_name='rates')
    min_weight = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    max_weight = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    base_cost = models.DecimalField(max_digits=12, decimal_places=2)
    cost_per_kg = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    estimated_days = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'shipping_rate'

    def __str__(self):
        return f"{self.carrier.name} - {self.shipping_zone.name}"


class Shipment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('picked_up', 'Picked Up'),
        ('in_transit', 'In Transit'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('failed', 'Failed'),
        ('returned', 'Returned'),
    ]

    shipment_number = models.CharField(max_length=50, unique=True)
    order_id = models.IntegerField()
    order_number = models.CharField(max_length=50, blank=True, null=True)
    customer_id = models.IntegerField(blank=True, null=True)
    carrier = models.ForeignKey(Carrier, on_delete=models.SET_NULL, blank=True, null=True, related_name='shipments')
    tracking_number = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    shipping_address_id = models.IntegerField(blank=True, null=True)
    ship_date = models.DateTimeField(blank=True, null=True)
    delivery_date = models.DateTimeField(blank=True, null=True)
    estimated_delivery = models.DateTimeField(blank=True, null=True)
    actual_weight = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    shipping_cost = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    class Meta:
        db_table = 'shipment'
        ordering = ['-ship_date']

    def __str__(self):
        return f"Shipment {self.shipment_number}"

    def save(self, *args, **kwargs):
        if not self.shipment_number:
            self.shipment_number = f"SHP{timezone.now().strftime('%Y%m%d%H%M%S')}{uuid.uuid4().hex[:4].upper()}"
        super().save(*args, **kwargs)
