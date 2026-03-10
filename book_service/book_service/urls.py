from django.urls import path, include
urlpatterns = [
    path('api/books/', include('book.urls')),
]
