from django.urls import path
from .views import LoginAPIView, ProtectedAPIView,RegisterAPIView
from rest_framework_simplejwt.views import TokenRefreshView
urlpatterns = [
    path('auth/register/', RegisterAPIView.as_view(), name='register'),
    path('auth/login/', LoginAPIView.as_view(), name='login'),
    path('auth/protected/', ProtectedAPIView.as_view(), name='protected'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
