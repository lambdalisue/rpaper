import uuid
import datetime
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils import formats
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from thumbnailfield.fields import ThumbnailField

from rpaper.core.utils import validate_on_save
from rpaper.core.fields.hashids import HashidsField


class Instrument(models.Model):
    hashid = HashidsField(
        verbose_name=_('Hashids'),
        primary_key=True,
        hashids_salt="%s:reservations:instrument" % settings.HASHIDS_SOLT,
        hashids_min_length=8,
    )
    name = models.CharField(_('Name'), max_length=255)
    remarks = models.TextField(_("Remarks"), blank=True)
    thumbnail = ThumbnailField(
        _("Thumbnail"),
        upload_to="reservations/instrument/thumbnails",
        blank=True,
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Owner"),
        related_name="instruments",
        editable=False,
    )

    ipaddress = models.GenericIPAddressField(
        _("IPAddress"),
        editable=False,
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Modified at"), auto_now=True)

    class Meta:
        verbose_name = _("Instrument")
        verbose_name_plural = _("Instruments")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('reservations:instruments-detail', kwargs=dict(
            pk=self.pk,
        ))


class ReservationManager(models.Manager):
    """A management class of Reservation model"""

    def _may_collide_with(self, reservation):
        # There is no reservation which time span is greater than threshold
        return self.filter(
            instrument=reservation.instrument,
            start_at__gt=reservation.start_at - Reservation.TIMESPAN_THRESHOLD,
            end_at__lt=reservation.end_at + Reservation.TIMESPAN_THRESHOLD,
        )

    def collide_with(self, reservation):
        """Return reservations queryset which collide with a reservation"""
        qs = self._may_collide_with(reservation)
        reservation_ids = (
            r.pk for r in qs if reservation.is_collided(r)
        )
        return self.filter(pk__in=reservation_ids)


@validate_on_save
class Reservation(models.Model):
    TIMESPAN_MAX_HOURS = 24
    TIMESPAN_THRESHOLD = datetime.timedelta(
        hours=TIMESPAN_MAX_HOURS
    )

    hashid = HashidsField(
        verbose_name=_("Hashid"),
        primary_key=True,
        hashids_salt="%s:reservations:reservation" % settings.HASHIDS_SOLT,
        hashids_min_length=8,
    )
    name = models.CharField(_('Name'), max_length=255)
    contact = models.CharField(_('Contact'), max_length=255)
    remarks = models.TextField(_("Remarks"), blank=True)

    instrument = models.ForeignKey(
        Instrument,
        verbose_name=_("Instrument"),
        related_name="reservations",
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Owner"),
        related_name="reservations",
        editable=False,
        blank=True,
        null=True,
    )

    start_at = models.DateTimeField(_("Start at"))
    end_at = models.DateTimeField(_("End at"))

    credential = models.UUIDField(
        _("Credential"),
        default=uuid.uuid4,
        editable=False,
    )
    ipaddress = models.GenericIPAddressField(
        _("IPAddress"),
        editable=False,
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Modified at"), auto_now=True)

    objects = ReservationManager()

    class Meta:
        verbose_name = _("Reservation")
        verbose_name_plural = _("Reservations")
        ordering = (
            'start_at',
            'end_at',
            'name',
        )

    def __str__(self):
        return _(
            "%(timespan)s by %(name)s",
        ) % dict(
            timespan=self.get_timespan_display(),
            name=self.name,
        )

    def is_collided(self, other):
        """Return if the reservation is collided with other"""
        if self.end_at <= other.start_at or other.end_at <= self.start_at:
            return False
        return True

    def get_timespan_display(self):
        """Return a human readable time-span string"""
        if self.start_at.day == self.end_at.day:
            return _("%(date)s %(start_at)s to %(end_at)s") % dict(
                date=formats.date_format(self.start_at, 'DATE_FORMAT'),
                start_at=formats.date_format(self.start_at, 'TIME_FORMAT'),
                end_at=formats.date_format(self.end_at, 'TIME_FORMAT'),
            )
        else:
            return _("%(start_at)s to %(end_at)s") % dict(
                start_at=formats.date_format(self.start_at, 'DATETIME_FORMAT'),
                end_at=formats.date_format(self.end_at, 'DATETIME_FORMAT'),
            )

    def clean(self):
        if self.start_at is None or self.end_at is None:
            return
        self._validate_timespan()
        self._validate_collision()

    def _validate_timespan(self):
        if self.end_at <= self.start_at:
            raise ValidationError(
                _("'end_at' could not be a greater value than 'start_at'"),
                code='invalid',
            )
        elif self.end_at - self.start_at > type(self).TIMESPAN_THRESHOLD:
            raise ValidationError(
                _('The time-span could not be over %(threshold)d hours.'),
                code='invalid',
                params={'threshold': type(self).TIMESPAN_MAX_HOURS},
            )

    def _validate_collision(self):
        qs = Reservation.objects.collide_with(self)
        if qs.count() > 0:
            raise ValidationError(
                _("The reservation collide with %(reservation)s"),
                code='invalid',
                params={'reservation': qs.first()},
            )
