from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CarrierViewSet, ShippingZoneViewSet, ShippingRateViewSet, ShipmentViewSet

router = DefaultRouter()
router.register(r'carriers', CarrierViewSet)
router.register(r'zones', ShippingZoneViewSet)
router.register(r'rates', ShippingRateViewSet)
router.register(r'', ShipmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
