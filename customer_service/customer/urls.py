from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet, ShippingAddressViewSet

router = DefaultRouter()
router.register(r'addresses', ShippingAddressViewSet)
router.register(r'', CustomerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
