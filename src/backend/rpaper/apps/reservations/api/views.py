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
    ThingSerializer,
    RecordSerializer,
    RecordSerializerWithCredential,
)
from ..models import (
    Thing,
    Record,
)
from ..filters import RecordFilter


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


class ThingAPIViewMixin:
    serializer_class = ThingSerializer
    queryset = Thing.objects.all()


class ThingCreateAPIView(ThingAPIViewMixin, CreateAPIView):
    permission_classes = (
        DjangoModelPermissions,
    )

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(
            owner=user,
            ipaddress=get_client_ip(self.request),
        )


class ThingRetrieveUpdateDestroyAPIView(ThingAPIViewMixin,
                                        RetrieveUpdateDestroyAPIView):
    permission_classes = (
        DjangoObjectPermissionsOrAnonReadOnly,
    )


class RecordAPIViewMixin:
    serializer_class = RecordSerializer

    def get_thing(self):
        thing_pk = self.kwargs['thing_pk']
        return get_object_or_404(Thing, pk=thing_pk)

    def get_queryset(self):
        return Record.objects.filter(
            thing=self.get_thing(),
        )


class RecordListCreateAPIView(RecordAPIViewMixin,
                              ListCreateAPIView):
    queryset = Thing.objects.all()
    permission_classes = (
        DjangoModelPermissionsOrAnonReadOnly,
    )
    filter_class = RecordFilter

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(
            owner=(user if user.is_authenticated() else None),
            ipaddress=get_client_ip(self.request),
            thing=self.get_thing(),
        )

    def get_serializer_class(self):
        if self.request.method == 'POST':
            # Return 'credential' when the object has created
            return RecordSerializerWithCredential
        return RecordSerializer


class RecordRetrieveUpdateDestroyAPIView(RecordAPIViewMixin,
                                         RetrieveUpdateDestroyAPIView):
    permission_classes = (
        DjangoObjectPermissionsOrAnonReadOnly,
    )

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            # Return 'credential' when the object has updated
            return RecordSerializerWithCredential
        return RecordSerializer
