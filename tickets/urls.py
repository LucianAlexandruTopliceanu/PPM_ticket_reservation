from django.urls import path
from .views import (
    EventListCreateView,
    EventRetrieveUpdateDestroyView,
    ReservationCreateView,
    UserReservationsListView,
    ReservationCancelView,
    EventSearchView
)

urlpatterns = [
    # Gestione eventi
    path('events/', EventListCreateView.as_view(), name='event-list'),
    path('events/<int:pk>/', EventRetrieveUpdateDestroyView.as_view(), name='event-detail'),

    # Ricerca eventi (aggiuntivo)
    path('events/search/', EventSearchView.as_view(), name='event-search'),

    # Prenotazioni
    path('reservations/', ReservationCreateView.as_view(), name='reservation-create'),
    path('reservations/my/', UserReservationsListView.as_view(), name='my-reservations'),
    path('reservations/<int:pk>/cancel/', ReservationCancelView.as_view(), name='reservation-cancel'),

]