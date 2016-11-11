from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from .views import (
    InstrumentCreateAPIView,
    InstrumentRetrieveUpdateDestroyAPIView,
    ReservationListCreateAPIView,
    ReservationRetrieveUpdateDestroyAPIView,
)


urlpatterns = [
    url(r'^instruments/$',
        InstrumentCreateAPIView.as_view(),
        name='instruments-list'),
    url(r'^instruments/(?P<pk>\w+)/$',
        InstrumentRetrieveUpdateDestroyAPIView.as_view(),
        name='instruments-detail'),
    url(r'^instruments/(?P<instrument_pk>\w+)/reservations/$',
        ReservationListCreateAPIView.as_view(),
        name='reservations-list'),
    url(r'^instruments/(?P<instrument_pk>\w+)/reservations/(?P<pk>\w+)/$',
        ReservationRetrieveUpdateDestroyAPIView.as_view(),
        name='reservations-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])
