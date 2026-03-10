from django.urls import path, include
urlpatterns = [
    path('api/recommendations/', include('recommender.urls')),
]
