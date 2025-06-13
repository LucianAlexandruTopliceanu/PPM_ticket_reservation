from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.db.models import F

from . import serializers, models
from .models import Event, Reservation
from .serializers import EventSerializer, ReservationSerializer
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.db.models import Q

class EventListCreateView(generics.ListCreateAPIView):
    """View per listare e creare eventi"""
    queryset = Event.objects.filter(date__gte=timezone.now())
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filterset_fields = ['organizer', 'date', 'location']
    search_fields = ['title', 'description', 'location']

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)


class EventRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """View per dettaglio, modifica e cancellazione eventi"""
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAdminUser() | permissions.IsAuthenticated()]
        return super().get_permissions()


class ReservationCreateView(generics.CreateAPIView):
    """View per creare prenotazioni"""
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        event = serializer.validated_data['event']
        seats = serializer.validated_data['seats']

        if seats > event.available_seats:
            raise serializers.ValidationError(
                {"seats": "Non ci sono abbastanza posti disponibili."}
            )

        # Transazione atomica per evitare race conditions
        Event.objects.filter(id=event.id).update(
            available_seats=F('available_seats') - seats
        )
        serializer.save(user=self.request.user, is_confirmed=True)


class UserReservationsListView(generics.ListAPIView):
    """View per listare le prenotazioni dell'utente"""
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Reservation.objects.filter(
            user=self.request.user,
            event__date__gte=timezone.now()
        ).select_related('event')


class ReservationCancelView(generics.DestroyAPIView):
    """View per cancellare prenotazioni"""
    queryset = Reservation.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj = get_object_or_404(Reservation, pk=self.kwargs['pk'])
        if obj.user != self.request.user and not self.request.user.is_staff:
            raise permissions.PermissionDenied(
                "Non hai i permessi per cancellare questa prenotazione."
            )
        return obj

    def perform_destroy(self, instance):
        # Ripristina i posti disponibili
        Event.objects.filter(id=instance.event.id).update(
            available_seats=F('available_seats') + instance.seats
        )
        instance.delete()


class EventSearchView(generics.ListAPIView):
    """View aggiuntiva per ricerca eventi"""
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Event.objects.filter(date__gte=timezone.now())

        search_term = self.request.query_params.get('search', None)
        if search_term:
            queryset = queryset.filter(
                Q(title__icontains=search_term) |
                Q(description__icontains=search_term) |
                Q(location__icontains=search_term)
            )

        return queryset