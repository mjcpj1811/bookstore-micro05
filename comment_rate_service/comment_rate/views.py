import requests
from django.conf import settings
from django.db.models import Avg
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Review, ReviewImage, ReviewReply
from .serializers import ReviewSerializer, ReviewImageSerializer, ReviewReplySerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.prefetch_related('images', 'replies')
    serializer_class = ReviewSerializer

    def get_queryset(self):
        qs = Review.objects.prefetch_related('images', 'replies')
        book_id = self.request.query_params.get('book_id')
        if book_id:
            qs = qs.filter(book_id=book_id)
        customer_id = self.request.query_params.get('customer_id')
        if customer_id:
            qs = qs.filter(customer_id=customer_id)
        return qs

    def perform_create(self, serializer):
        """After creating a review, update book rating in book-service."""
        review = serializer.save()
        self._update_book_rating(review.book_id)

    def perform_update(self, serializer):
        review = serializer.save()
        self._update_book_rating(review.book_id)

    def perform_destroy(self, instance):
        book_id = instance.book_id
        instance.delete()
        self._update_book_rating(book_id)

    def _update_book_rating(self, book_id):
        """Recalculate and push average rating to book-service."""
        avg = Review.objects.filter(book_id=book_id).aggregate(avg=Avg('rating'))['avg']
        if avg is not None:
            try:
                requests.patch(
                    f"{settings.SERVICE_URLS['BOOK_SERVICE']}/api/books/{book_id}/",
                    json={'rating': round(float(avg), 2)},
                    timeout=5,
                )
            except requests.RequestException:
                pass

    @action(detail=False, methods=['get'])
    def book_rating(self, request):
        """Get average rating for a book."""
        book_id = request.query_params.get('book_id')
        if not book_id:
            return Response({'error': 'book_id required'}, status=status.HTTP_400_BAD_REQUEST)
        avg = Review.objects.filter(book_id=book_id).aggregate(avg=Avg('rating'))['avg']
        count = Review.objects.filter(book_id=book_id).count()
        return Response({'book_id': int(book_id), 'average_rating': avg or 0, 'review_count': count})

    @action(detail=True, methods=['post'])
    def helpful(self, request, pk=None):
        review = self.get_object()
        review.helpful_count += 1
        review.save(update_fields=['helpful_count'])
        return Response({'helpful_count': review.helpful_count})

    @action(detail=True, methods=['post'])
    def report(self, request, pk=None):
        review = self.get_object()
        review.report_count += 1
        review.save(update_fields=['report_count'])
        return Response({'report_count': review.report_count})


class ReviewReplyViewSet(viewsets.ModelViewSet):
    queryset = ReviewReply.objects.all()
    serializer_class = ReviewReplySerializer
