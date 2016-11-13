from django.contrib.auth.models import User
from rest_framework import serializers
from ..models import (
    Instrument,
    Reservation,
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
        )


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = (
            'instrument',
            'pk',
            'name',
            'contact',
            'remarks',
            'start_at',
            'end_at',
        )
        read_only_fields = ('instrument', 'pk',)

    pk = serializers.RegexField('\w+', read_only=True)


class ReservationSerializerWithCredential(ReservationSerializer):
    class Meta:
        model = Reservation
        fields = (
            'instrument',
            'pk',
            'name',
            'contact',
            'remarks',
            'start_at',
            'end_at',
            'credential',
        )
        read_only_fields = ('instrument', 'pk', 'credential')


class InstrumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instrument
        fields = (
            'pk',
            'name',
            'remarks',
            'thumbnail',
            'owner',
            'reservations',
        )

    pk = serializers.RegexField('\w+', read_only=True)
    owner = UserSerializer(many=False, read_only=True)
    reservations = ReservationSerializer(many=True, read_only=True)
