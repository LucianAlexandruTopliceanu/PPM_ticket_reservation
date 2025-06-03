from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from .serializers import (
    CustomUserSerializer,
    CustomTokenObtainPairSerializer,
    PasswordResetSerializer
)
from django.core.mail import send_mail
from django.conf import settings

CustomUser = get_user_model()


class UserCreateView(generics.CreateAPIView):
    """View per la registrazione nuovi utenti"""
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        # Invio email di benvenuto (opzionale)
        send_mail(
            'Benvenuto nel Ticket Reservation System',
            f'Ciao {user.username}, la tua registrazione è avvenuta con successo!',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=True,
        )


class UserDetailView(generics.RetrieveUpdateAPIView):
    """View per visualizzare e modificare il profilo utente"""
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class CustomTokenObtainPairView(TokenObtainPairView):
    """View personalizzata per il login JWT"""
    serializer_class = CustomTokenObtainPairSerializer


class PasswordResetView(generics.GenericAPIView):
    """View per la richiesta reset password"""
    serializer_class = PasswordResetSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": "Password reset e-mail has been sent."},
            status=status.HTTP_200_OK
        )


class PasswordResetConfirmView(generics.GenericAPIView):
    """View per la conferma reset password"""
    permission_classes = [permissions.AllowAny]

    def post(self, request, uidb64, token):
        # Implementazione della logica di reset
        # (utilizzando i token generati da Django)
        return Response(
            {"detail": "Password has been reset with the new password."},
            status=status.HTTP_200_OK
        )