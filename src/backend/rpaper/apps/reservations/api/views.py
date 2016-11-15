from django.shortcuts import get_object_or_404
from rest_framework.permissions import (
    SAFE_METHODS,
    DjangoModelPermissions,
    DjangoObjectPermissions,
    DjangoModelPermissionsOrAnonReadOnly,
)
from rest_framework.generics import (
    CreateAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rpaper.core.utils import get_client_ip
from .serializer import (
    InstrumentSerializer,
    ReservationSerializer,
    ReservationSerializerWithCredential,
)
from ..models import (
    Instrument,
    Reservation,
)
from ..filters import ReservationFilter


class DjangoObjectPermissionsOrAnonReadOnly(DjangoObjectPermissions):
    authenticated_users_only = False

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return super().has_object_permission(request, view, obj)


class InstrumentAPIViewMixin:
    serializer_class = InstrumentSerializer
    queryset = Instrument.objects.all()


class InstrumentCreateAPIView(InstrumentAPIViewMixin, CreateAPIView):
    permission_classes = (
        DjangoModelPermissions,
    )

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(
            owner=user,
            ipaddress=get_client_ip(self.request),
        )


class InstrumentRetrieveUpdateDestroyAPIView(InstrumentAPIViewMixin,
                                             RetrieveUpdateDestroyAPIView):
    permission_classes = (
        DjangoObjectPermissionsOrAnonReadOnly,
    )


class ReservationAPIViewMixin:
    serializer_class = ReservationSerializer

    def get_instrument(self):
        instrument_pk = self.kwargs['instrument_pk']
        return get_object_or_404(Instrument, pk=instrument_pk)

    def get_queryset(self):
        return Reservation.objects.filter(
            instrument=self.get_instrument(),
        )


class ReservationListCreateAPIView(ReservationAPIViewMixin,
                                   ListCreateAPIView):
    queryset = Instrument.objects.all()
    permission_classes = (
        DjangoModelPermissionsOrAnonReadOnly,
    )
    filter_class = ReservationFilter

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(
            owner=(user if user.is_authenticated() else None),
            ipaddress=get_client_ip(self.request),
            instrument=self.get_instrument(),
        )

    def get_serializer_class(self):
        if self.request.method == 'POST':
            # Return 'credential' when the object has created
            return ReservationSerializerWithCredential
        return ReservationSerializer


class ReservationRetrieveUpdateDestroyAPIView(ReservationAPIViewMixin,
                                              RetrieveUpdateDestroyAPIView):
    permission_classes = (
        DjangoObjectPermissionsOrAnonReadOnly,
    )

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            # Return 'credential' when the object has updated
            return ReservationSerializerWithCredential
        return ReservationSerializer
