from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.db.models import F
from . import serializers, models
from .models import Event, Reservation, Payment
from .permissions import IsOrganizerOrAdmin
from .serializers import EventSerializer, ReservationSerializer, PaymentSerializer
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


from rest_framework.exceptions import ValidationError


class EventRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """View per dettaglio, modifica e cancellazione eventi"""
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self):
        event = get_object_or_404(Event, pk=self.kwargs['pk'])
        return event

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsOrganizerOrAdmin()]
        return super().get_permissions()

    def perform_update(self, serializer):
        instance = self.get_object()  # L'evento esistente
        new_total_seats = serializer.validated_data.get('total_seats', instance.total_seats)

        # Controllo che i nuovi posti totali non siano minori di quelli già prenotati
        seats_already_reserved = instance.total_seats - instance.available_seats
        if new_total_seats < seats_already_reserved:
            raise ValidationError({
                'total_seats': f'Non puoi impostare meno di {seats_already_reserved} posti totali '
                               f'(già {seats_already_reserved} prenotati)'
            })

        # Calcola la nuova disponibilità
        if 'total_seats' in serializer.validated_data:
            difference = new_total_seats - instance.total_seats
            serializer.validated_data['available_seats'] = instance.available_seats + difference

        # Gestione del prezzo
        new_price = serializer.validated_data.get('price', instance.price)
        if new_price < 0:
            raise ValidationError({
                'price': 'Il prezzo non può essere negativo'
            })

        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()


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


class PaymentCreateView(generics.CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        reservation_id = request.data.get('reservation')
        try:
            reservation = Reservation.objects.get(id=reservation_id, user=request.user)
        except Reservation.DoesNotExist:
            return Response(
                {"error": "Prenotazione non trovata o non autorizzata"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Calcola il totale (prezzo evento * numero posti)
        total_amount = reservation.event.price * reservation.seats

        payment_data = {
            'reservation': reservation.id,
            'amount': total_amount,
            'payment_method': request.data.get('payment_method', 'card'),
            'status': 'pending'
        }

        serializer = self.get_serializer(data=payment_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Qui andrebbe integrato il vero processore di pagamento
        # Per ora simulo un pagamento riuscito
        payment = serializer.instance
        payment.status = 'completed'
        payment.transaction_id = f"SIM{payment.id:08d}"
        payment.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
