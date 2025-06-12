from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from .serializers import (
    CustomUserSerializer,
    CustomTokenObtainPairSerializer,
)

CustomUser = get_user_model()


class UserCreateView(generics.CreateAPIView):
    """View per la registrazione nuovi utenti"""
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.AllowAny]

    @csrf_exempt
    def perform_create(self, serializer):
        user = serializer.save()


class UserDetailView(generics.RetrieveUpdateAPIView):
    """View per visualizzare e modificare il profilo utente"""
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class CustomTokenObtainPairView(TokenObtainPairView):
    """View personalizzata per il login JWT"""
    serializer_class = CustomTokenObtainPairSerializer
