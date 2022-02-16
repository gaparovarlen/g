from django.urls import path
from .views import CustomUserCreate
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


urlpatterns = [
    path('register/', CustomUserCreate.as_view(), name="create_user"),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]