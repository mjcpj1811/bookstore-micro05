from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaymentMethodViewSet, PaymentViewSet

router = DefaultRouter()
router.register(r'methods', PaymentMethodViewSet)
router.register(r'', PaymentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
