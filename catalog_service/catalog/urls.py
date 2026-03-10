from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PublisherViewSet, AuthorViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r'publishers', PublisherViewSet)
router.register(r'authors', AuthorViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
