from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView
from .views import (
    UserCreateView,
    UserDetailView,
    CustomTokenObtainPairView,
)

urlpatterns = [
    # Registrazione nuovo utente
    path('register/', UserCreateView.as_view(), name='user-register'),

    # Login JWT
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),

    # Profilo utente
    path('me/', UserDetailView.as_view(), name='user-detail'),

    # Verifica token
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]