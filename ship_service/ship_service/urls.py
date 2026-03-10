from django.urls import path, include
urlpatterns = [
    path('api/shipments/', include('ship.urls')),
]
