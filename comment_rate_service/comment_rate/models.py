from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(models.Model):
    book_id = models.IntegerField()
    customer_id = models.IntegerField()
    order_id = models.IntegerField(blank=True, null=True)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=255, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    helpful_count = models.IntegerField(default=0)
    report_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'review'
        ordering = ['-created_at']
        unique_together = ['book_id', 'customer_id']

    def __str__(self):
        return f"Review for book {self.book_id} by customer {self.customer_id}"


class ReviewImage(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='images')
    image_url = models.URLField(max_length=500)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'review_image'

    def __str__(self):
        return f"Image for review #{self.review.id}"


class ReviewReply(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='replies')
    user_id = models.IntegerField()
    reply_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'review_reply'
        ordering = ['created_at']
