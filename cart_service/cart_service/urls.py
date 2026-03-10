from django.urls import path, include
urlpatterns = [
    path('api/carts/', include('cart.urls')),
]
