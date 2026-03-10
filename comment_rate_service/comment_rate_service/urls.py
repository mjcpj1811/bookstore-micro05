from django.urls import path, include
urlpatterns = [
    path('api/reviews/', include('comment_rate.urls')),
]
