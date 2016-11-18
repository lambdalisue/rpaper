from django.conf.urls import url

from .views import ThingDetailView


urlpatterns = [
    url(r'^(?P<pk>\w+)/$',
        ThingDetailView.as_view(),
        name='reservations-thing'),
]
