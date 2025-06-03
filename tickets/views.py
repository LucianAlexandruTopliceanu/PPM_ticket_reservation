
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Event, Reservation
from .serializers import EventSerializer, ReservationSerializer
from users.models import CustomUser


class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)


class EventRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ReservationCreateView(generics.CreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        event = serializer.validated_data['event']
        seats = serializer.validated_data['seats']

        if seats > event.available_seats:
            raise serializers.ValidationError("Not enough seats available")

        event.available_seats -= seats
        event.save()

        serializer.save(user=self.request.user, is_confirmed=True)


class UserReservationsListView(generics.ListAPIView):
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)