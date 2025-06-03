# users/urls.py
from django.urls import path
from .views import UserCreateView, UserDetailView, CustomTokenObtainPairView

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='user-register'),
    path('me/', UserDetailView.as_view(), name='user-detail'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
]