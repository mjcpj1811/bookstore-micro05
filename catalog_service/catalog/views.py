from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Publisher, Author, Category
from .serializers import PublisherSerializer, AuthorSerializer, CategorySerializer


class PublisherViewSet(viewsets.ModelViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def get_queryset(self):
        qs = Author.objects.all()
        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(name__icontains=search)
        return qs


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        qs = Category.objects.all()
        active_only = self.request.query_params.get('active')
        if active_only:
            qs = qs.filter(is_active=True)
        return qs

    @action(detail=False, methods=['get'])
    def tree(self, request):
        """Return category tree (only root categories)."""
        roots = Category.objects.filter(parent_category__isnull=True, is_active=True)
        serializer = self.get_serializer(roots, many=True)
        return Response(serializer.data)
