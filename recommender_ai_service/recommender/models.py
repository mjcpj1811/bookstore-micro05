from django.db import models


class UserBehavior(models.Model):
    ACTION_TYPE_CHOICES = [
        ('view', 'View'),
        ('click', 'Click'),
        ('add_to_cart', 'Add to Cart'),
        ('purchase', 'Purchase'),
        ('wishlist', 'Wishlist'),
        ('review', 'Review'),
        ('search', 'Search'),
    ]

    customer_id = models.IntegerField()
    book_id = models.IntegerField()
    action_type = models.CharField(max_length=20, choices=ACTION_TYPE_CHOICES)
    session_id = models.CharField(max_length=255, blank=True, null=True)
    device_type = models.CharField(max_length=50, blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_behavior'
        ordering = ['-timestamp']

    def __str__(self):
        return f"Customer {self.customer_id} - {self.action_type} - Book {self.book_id}"


class Recommendation(models.Model):
    customer_id = models.IntegerField()
    book_id = models.IntegerField()
    score = models.DecimalField(max_digits=8, decimal_places=6, blank=True, null=True)
    reason = models.TextField(blank=True, null=True)
    generated_at = models.DateTimeField(auto_now_add=True)
    clicked_at = models.DateTimeField(blank=True, null=True)
    is_converted = models.BooleanField(default=False)

    class Meta:
        db_table = 'recommendation'
        ordering = ['-score', '-generated_at']

    def __str__(self):
        return f"Recommend book {self.book_id} to customer {self.customer_id}"
