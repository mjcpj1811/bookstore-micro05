from django.db import models
from django.utils import timezone
import uuid


class PaymentMethod(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    icon_url = models.URLField(max_length=500, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    processing_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    display_order = models.IntegerField(default=0)

    class Meta:
        db_table = 'payment_method'
        ordering = ['display_order']

    def __str__(self):
        return self.name


class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
        ('cancelled', 'Cancelled'),
    ]

    payment_number = models.CharField(max_length=50, unique=True)
    order_id = models.IntegerField()
    order_number = models.CharField(max_length=50, blank=True, null=True)
    customer_id = models.IntegerField(blank=True, null=True)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=255, blank=True, null=True)
    payment_date = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(blank=True, null=True)
    failure_reason = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'payment'
        ordering = ['-payment_date']

    def __str__(self):
        return f"Payment {self.payment_number}"

    def save(self, *args, **kwargs):
        if not self.payment_number:
            self.payment_number = f"PAY{timezone.now().strftime('%Y%m%d%H%M%S')}{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)
