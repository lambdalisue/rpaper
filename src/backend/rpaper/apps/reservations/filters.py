from django_filters import rest_framework as filters
from .models import Reservation


class ReservationFilter(filters.FilterSet):
    since = filters.IsoDateTimeFilter(
        name='end_at',
        lookup_expr='gte',
    )
    until = filters.IsoDateTimeFilter(
        name='start_at',
        lookup_expr='lte',
    )

    class Meta:
        model = Reservation
        fields = ['since', 'until']
