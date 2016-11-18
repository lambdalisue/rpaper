from django.contrib.auth.models import User
from rest_framework import serializers
from ..models import (
    Thing,
    Record,
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
        )


class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = (
            'thing',
            'pk',
            'name',
            'contact',
            'remarks',
            'start_at',
            'end_at',
        )
        read_only_fields = ('thing', 'pk',)

    pk = serializers.RegexField('\w+', read_only=True)


class RecordSerializerWithCredential(RecordSerializer):
    class Meta:
        model = Record
        fields = (
            'thing',
            'pk',
            'name',
            'contact',
            'remarks',
            'start_at',
            'end_at',
            'credential',
        )
        read_only_fields = ('thing', 'pk', 'credential')


class ThingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thing
        fields = (
            'pk',
            'name',
            'remarks',
            'thumbnail',
            'owner',
        )

    pk = serializers.RegexField('\w+', read_only=True)
    owner = UserSerializer(many=False, read_only=True)
