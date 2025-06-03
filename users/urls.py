from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView
from .views import (
    UserCreateView,
    UserDetailView,
    CustomTokenObtainPairView,
    PasswordResetConfirmView,
    PasswordResetView,
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

    # TODO: Reset password
    path('password/reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password/reset/confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
]