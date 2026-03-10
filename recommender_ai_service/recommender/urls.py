from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserBehaviorViewSet, RecommendationViewSet

router = DefaultRouter()
router.register(r'behaviors', UserBehaviorViewSet)
router.register(r'', RecommendationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
