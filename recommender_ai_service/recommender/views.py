import requests
from collections import Counter
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import UserBehavior, Recommendation
from .serializers import UserBehaviorSerializer, RecommendationSerializer


class UserBehaviorViewSet(viewsets.ModelViewSet):
    queryset = UserBehavior.objects.all()
    serializer_class = UserBehaviorSerializer

    def get_queryset(self):
        qs = UserBehavior.objects.all()
        customer_id = self.request.query_params.get('customer_id')
        if customer_id:
            qs = qs.filter(customer_id=customer_id)
        book_id = self.request.query_params.get('book_id')
        if book_id:
            qs = qs.filter(book_id=book_id)
        return qs


class RecommendationViewSet(viewsets.ModelViewSet):
    queryset = Recommendation.objects.all()
    serializer_class = RecommendationSerializer

    def get_queryset(self):
        qs = Recommendation.objects.all()
        customer_id = self.request.query_params.get('customer_id')
        if customer_id:
            qs = qs.filter(customer_id=customer_id)
        return qs

    @action(detail=False, methods=['post'])
    def generate(self, request):
        """
        Simple AI recommendation: based on user behavior, 
        recommend popular books the user hasn't interacted with.
        """
        customer_id = request.data.get('customer_id')
        if not customer_id:
            return Response({'error': 'customer_id required'}, status=status.HTTP_400_BAD_REQUEST)

        # Get books user already interacted with
        user_books = set(
            UserBehavior.objects.filter(customer_id=customer_id)
            .values_list('book_id', flat=True)
        )

        # Get popular books from all behaviors (collaborative filtering)
        popular = (
            UserBehavior.objects.filter(action_type__in=['purchase', 'add_to_cart', 'view'])
            .exclude(book_id__in=user_books)
            .values_list('book_id', flat=True)
        )
        book_counts = Counter(popular)
        top_books = [book_id for book_id, _ in book_counts.most_common(8)]

        # Fallback: if not enough recommendations, fetch random books from book service
        if len(top_books) < 5:
            try:
                resp = requests.get(f"{settings.SERVICE_URLS.get('BOOK_SERVICE', 'http://book-service:8000')}/api/books/", timeout=5)
                if resp.status_code == 200:
                    all_books = resp.json().get('results', resp.json()) if isinstance(resp.json(), dict) else resp.json()
                    import random
                    candidates = [b['id'] for b in all_books if b['id'] not in user_books and b['id'] not in top_books]
                    random.shuffle(candidates)
                    top_books.extend(candidates[:8 - len(top_books)])
            except Exception:
                pass

        # Clear old recommendations
        Recommendation.objects.filter(customer_id=customer_id).delete()

        # Create new recommendations
        recommendations = []
        for rank, book_id in enumerate(top_books):
            score = 1.0 - (rank * 0.1)
            rec = Recommendation.objects.create(
                customer_id=customer_id,
                book_id=book_id,
                score=max(score, 0.1),
                reason='Based on popular items and collaborative filtering',
            )
            recommendations.append(rec)

        return Response(RecommendationSerializer(recommendations, many=True).data)

    @action(detail=True, methods=['post'])
    def click(self, request, pk=None):
        rec = self.get_object()
        from django.utils import timezone
        rec.clicked_at = timezone.now()
        rec.save(update_fields=['clicked_at'])
        return Response(RecommendationSerializer(rec).data)

    @action(detail=True, methods=['post'])
    def convert(self, request, pk=None):
        rec = self.get_object()
        rec.is_converted = True
        rec.save(update_fields=['is_converted'])
        return Response(RecommendationSerializer(rec).data)
