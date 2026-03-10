from django.urls import path, include
urlpatterns = [
    path('', include('gateway.template_urls')),
    path('api/', include('gateway.urls')),
]
