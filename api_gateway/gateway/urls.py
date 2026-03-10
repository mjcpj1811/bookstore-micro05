from django.urls import path
from .views import (
    ApiRootView, StaffProxy, ManagerProxy, CustomerProxy, CatalogProxy,
    BookProxy, CartProxy, OrderProxy, ShipProxy, PayProxy,
    ReviewProxy, RecommendationProxy, ServiceHealthView,
)

urlpatterns = [
    # API root
    path('', ApiRootView.as_view(), name='api-root'),

    # Health check
    path('health/', ServiceHealthView.as_view(), name='health'),

    # Staff service
    path('staff/', StaffProxy.as_view(), name='staff-list'),
    path('staff/<path:path>', StaffProxy.as_view(), name='staff-detail'),

    # Manager service
    path('manager/', ManagerProxy.as_view(), name='manager-list'),
    path('manager/<path:path>', ManagerProxy.as_view(), name='manager-detail'),

    # Customer service
    path('customers/', CustomerProxy.as_view(), name='customer-list'),
    path('customers/<path:path>', CustomerProxy.as_view(), name='customer-detail'),

    # Catalog service (publishers, authors, categories)
    path('catalog/', CatalogProxy.as_view(), name='catalog-list'),
    path('catalog/<path:path>', CatalogProxy.as_view(), name='catalog-detail'),

    # Book service
    path('books/', BookProxy.as_view(), name='book-list'),
    path('books/<path:path>', BookProxy.as_view(), name='book-detail'),

    # Cart service
    path('carts/', CartProxy.as_view(), name='cart-list'),
    path('carts/<path:path>', CartProxy.as_view(), name='cart-detail'),

    # Order service
    path('orders/', OrderProxy.as_view(), name='order-list'),
    path('orders/<path:path>', OrderProxy.as_view(), name='order-detail'),

    # Ship service
    path('shipments/', ShipProxy.as_view(), name='ship-list'),
    path('shipments/<path:path>', ShipProxy.as_view(), name='ship-detail'),

    # Pay service
    path('payments/', PayProxy.as_view(), name='pay-list'),
    path('payments/<path:path>', PayProxy.as_view(), name='pay-detail'),

    # Comment/Rate service
    path('reviews/', ReviewProxy.as_view(), name='review-list'),
    path('reviews/<path:path>', ReviewProxy.as_view(), name='review-detail'),

    # Recommender AI service
    path('recommendations/', RecommendationProxy.as_view(), name='recommendation-list'),
    path('recommendations/<path:path>', RecommendationProxy.as_view(), name='recommendation-detail'),
]
