from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReviewViewSet, ReviewReplyViewSet

router = DefaultRouter()
router.register(r'replies', ReviewReplyViewSet)
router.register(r'', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
