from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, F
from .models import Book
from .serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    """Staff manages books. Full CRUD + search + stock management."""
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_queryset(self):
        qs = Book.objects.all()
        params = self.request.query_params

        # Filters
        is_active = params.get('is_active')
        if is_active is not None:
            qs = qs.filter(is_active=is_active.lower() == 'true')

        category_id = params.get('category_id')
        if category_id:
            qs = qs.filter(category_ids__contains=[int(category_id)])

        author_id = params.get('author_id')
        if author_id:
            qs = qs.filter(author_ids__contains=[int(author_id)])

        publisher_id = params.get('publisher_id')
        if publisher_id:
            qs = qs.filter(publisher_id=publisher_id)

        min_price = params.get('min_price')
        if min_price:
            qs = qs.filter(price__gte=min_price)

        max_price = params.get('max_price')
        if max_price:
            qs = qs.filter(price__lte=max_price)

        in_stock = params.get('in_stock')
        if in_stock:
            qs = qs.filter(stock__gt=0)

        # Search
        search = params.get('search')
        if search:
            qs = qs.filter(
                Q(title__icontains=search) |
                Q(isbn__icontains=search) |
                Q(description__icontains=search)
            )

        # Sort
        sort_by = params.get('sort_by') or params.get('sort') or '-created_at'
        sort_map = {
            'price_asc': 'price',
            'price_desc': '-price',
            'rating': '-rating',
            'bestseller': '-sold_count',
            'newest': '-created_at',
        }
        qs = qs.order_by(sort_map.get(sort_by, sort_by))
        return qs

    @action(detail=False, methods=['get'])
    def featured(self, request):
        limit = int(request.query_params.get('limit', 10))
        books = Book.objects.filter(is_active=True).order_by('-sold_count', '-rating')[:limit]
        return Response(BookSerializer(books, many=True).data)

    @action(detail=False, methods=['get'])
    def new_arrivals(self, request):
        limit = int(request.query_params.get('limit', 10))
        books = Book.objects.filter(is_active=True).order_by('-created_at')[:limit]
        return Response(BookSerializer(books, many=True).data)

    @action(detail=True, methods=['post'])
    def update_stock(self, request, pk=None):
        """Staff updates book stock."""
        book = self.get_object()
        quantity = request.data.get('quantity', 0)
        book.stock = F('stock') + int(quantity)
        book.save(update_fields=['stock'])
        book.refresh_from_db()
        return Response(BookSerializer(book).data)

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        book = self.get_object()
        book.is_active = False
        book.save()
        return Response({'status': 'deactivated'})
