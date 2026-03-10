from django.urls import path, include
urlpatterns = [
    path('api/manager/', include('manager.urls')),
]
