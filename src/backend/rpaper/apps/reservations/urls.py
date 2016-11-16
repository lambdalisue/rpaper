from django.conf.urls import url

from .views import InstrumentDetailView


urlpatterns = [
    url(r'^instrument/(?P<pk>\w+)/$',
        InstrumentDetailView.as_view(),
        name='reservations-instrument'),
]
