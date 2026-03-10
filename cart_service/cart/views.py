import requests
from decimal import Decimal
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_queryset(self):
        qs = Cart.objects.prefetch_related('items')
        customer_id = self.request.query_params.get('customer_id')
        if customer_id:
            qs = qs.filter(customer_id=customer_id)
        return qs

    @action(detail=False, methods=['get'])
    def my_cart(self, request):
        """Get cart by customer_id query param."""
        customer_id = request.query_params.get('customer_id')
        if not customer_id:
            return Response({'error': 'customer_id required'}, status=status.HTTP_400_BAD_REQUEST)
        cart, _ = Cart.objects.prefetch_related('items').get_or_create(customer_id=customer_id)
        return Response(CartSerializer(cart).data)

    @action(detail=True, methods=['post'])
    def add_item(self, request, pk=None):
        """Add book to cart. Fetches book info from book-service."""
        cart = self.get_object()
        book_id = request.data.get('book_id')
        quantity = int(request.data.get('quantity', 1))

        if not book_id:
            return Response({'error': 'book_id required'}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch book info from book-service
        book_title = ''
        price = request.data.get('price', 0)
        try:
            resp = requests.get(
                f"{settings.SERVICE_URLS['BOOK_SERVICE']}/api/books/{book_id}/",
                timeout=5,
            )
            if resp.status_code == 200:
                book_data = resp.json()
                book_title = book_data.get('title', '')
                price = book_data.get('discount_price') or book_data.get('price', price)
        except requests.RequestException:
            pass

        try:
            item = CartItem.objects.get(cart=cart, book_id=book_id)
            item.quantity += quantity
            item.price = Decimal(str(price))
            item.book_title = book_title
            item.save()
            created = False
        except CartItem.DoesNotExist:
            item = CartItem.objects.create(
                cart=cart,
                book_id=book_id,
                quantity=quantity,
                price=Decimal(str(price)),
                book_title=book_title,
            )
            created = True
        return Response(CartItemSerializer(item).data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def update_item(self, request, pk=None):
        """Update quantity of item in cart."""
        cart = self.get_object()
        book_id = request.data.get('book_id')
        quantity = int(request.data.get('quantity', 1))

        try:
            item = CartItem.objects.get(cart=cart, book_id=book_id)
        except CartItem.DoesNotExist:
            return Response({'error': 'Item not in cart'}, status=status.HTTP_404_NOT_FOUND)

        if quantity <= 0:
            item.delete()
            return Response({'status': 'removed'})

        item.quantity = quantity
        item.save()
        return Response(CartItemSerializer(item).data)

    @action(detail=True, methods=['post'])
    def remove_item(self, request, pk=None):
        """Remove a book from cart."""
        cart = self.get_object()
        book_id = request.data.get('book_id')
        deleted, _ = CartItem.objects.filter(cart=cart, book_id=book_id).delete()
        if deleted:
            return Response({'status': 'removed'})
        return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def clear(self, request, pk=None):
        """Clear all items from cart."""
        cart = self.get_object()
        cart.items.all().delete()
        return Response({'status': 'cart cleared'})
