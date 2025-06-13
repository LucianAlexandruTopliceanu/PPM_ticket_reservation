from rest_framework import serializers
from .models import Event, Reservation
from users.models import CustomUser
from django.utils import timezone


class EventSerializer(serializers.ModelSerializer):
    organizer = serializers.SlugRelatedField(
        slug_field='username',
        queryset=CustomUser.objects.all(),
        default=serializers.CurrentUserDefault()
    )
    is_past = serializers.SerializerMethodField()
    available_seats = serializers.IntegerField(read_only=True)

    class Meta:
        model = Event
        fields = (
            'id', 'title', 'description', 'date', 'location',
            'total_seats', 'available_seats', 'organizer', 'is_past'
        )
        read_only_fields = ('organizer', 'available_seats')

    def get_is_past(self, obj):
        return obj.date < timezone.now()

    def validate_date(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("La data dell'evento non può essere nel passato.")
        return value

    def validate_total_seats(self, value):
        if value <= 0:
            raise serializers.ValidationError("Il numero di posti deve essere positivo.")
        return value

    def create(self, validated_data):
        validated_data['available_seats'] = validated_data['total_seats']
        return super().create(validated_data)


class ReservationSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
        queryset=CustomUser.objects.all(),
        default=serializers.CurrentUserDefault()
    )
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())
    event_details = EventSerializer(source='event', read_only=True)
    can_cancel = serializers.SerializerMethodField()

    class Meta:
        model = Reservation
        fields = (
            'id', 'event', 'event_details', 'user', 'seats',
            'created_at', 'is_confirmed', 'can_cancel'
        )
        read_only_fields = ('user', 'created_at', 'is_confirmed')

    def get_can_cancel(self, obj):
        request = self.context.get('request')
        return (
                request and
                request.user == obj.user and
                obj.event.date > timezone.now()
        )

    def validate(self, data):
        if data['event'].date < timezone.now():
            raise serializers.ValidationError(
                {"event": "Non è possibile prenotare per un evento passato."}
            )

        if data['seats'] <= 0:
            raise serializers.ValidationError(
                {"seats": "Il numero di posti deve essere positivo."}
            )

        if data['seats'] > data['event'].available_seats:
            raise serializers.ValidationError(
                {"seats": "Posti disponibili insufficienti."}
            )

        return data


class EventAvailabilitySerializer(serializers.Serializer):
    date_from = serializers.DateTimeField(required=True)
    date_to = serializers.DateTimeField(required=True)

    def validate(self, data):
        if data['date_from'] > data['date_to']:
            raise serializers.ValidationError(
                "La data di inizio deve essere precedente alla data di fine."
            )
        return data