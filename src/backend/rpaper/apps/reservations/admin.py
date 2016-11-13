from django.contrib import admin
from rpaper.core.utils import get_client_ip
from .models import (
    Instrument,
    Reservation,
)


@admin.register(Instrument)
class InstrumentAdmin(admin.ModelAdmin):
    readonly_fields = ('pk', 'owner')

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'owner', None) is None:
            obj.owner = request.user
        if getattr(obj, 'ipaddress', None) is None:
            obj.ipaddress = get_client_ip(request)
        obj.save()


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    readonly_fields = ('pk', 'owner')

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'owner', None) is None:
            obj.owner = request.user
        if getattr(obj, 'ipaddress', None) is None:
            obj.ipaddress = get_client_ip(request)
        obj.save()
