from django.urls import path, include
urlpatterns = [
    path('api/payments/', include('pay.urls')),
]
