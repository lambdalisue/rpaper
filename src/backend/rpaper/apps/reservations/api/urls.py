from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from .views import (
    ThingCreateAPIView,
    ThingRetrieveUpdateDestroyAPIView,
    RecordListCreateAPIView,
    RecordRetrieveUpdateDestroyAPIView,
)


urlpatterns = [
    url(r'^$',
        ThingCreateAPIView.as_view(),
        name='things-list'),
    url(r'^(?P<pk>\w+)/$',
        ThingRetrieveUpdateDestroyAPIView.as_view(),
        name='things-detail'),
    url(r'^(?P<thing_pk>\w+)/records/$',
        RecordListCreateAPIView.as_view(),
        name='records-list'),
    url(r'^(?P<thing_pk>\w+)/records/(?P<pk>\w+)/$',
        RecordRetrieveUpdateDestroyAPIView.as_view(),
        name='records-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])
