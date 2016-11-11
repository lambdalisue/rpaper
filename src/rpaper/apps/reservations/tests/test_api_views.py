from operator import itemgetter, attrgetter
from django.test import TestCase, override_settings
from django.core.urlresolvers import reverse
from rest_framework.test import APIClient
from rpaper.core.storage.dummy import create_dummy_image
from ..models import Instrument, Reservation
from .factories import (
    UserFactory,
    InstrumentFactory,
    ReservationFactory,
)


@override_settings(
    DEFAULT_FILE_STORAGE='rpaper.core.storage.dummy.DummyStorage',
)
class InstrumentAPIView(TestCase):
    LIST_URL_NAME = 'reservations-api:instruments-list'
    DETAIL_URL_NAME = 'reservations-api:instruments-detail'

    def setUp(self):
        self.user = UserFactory()
        self.client = APIClient()

    def test_list(self):
        url = reverse(self.LIST_URL_NAME)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_detail(self):
        instrument = InstrumentFactory()
        url = reverse(self.DETAIL_URL_NAME, kwargs=dict(pk=instrument.pk))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(list(response.data.keys()), [
            'pk', 'name', 'remarks', 'thumbnail', 'owner', 'reservations',
        ])
        self.assertEqual(response.data['pk'], instrument.pk)

    def test_create_valid(self):
        self.client.force_authenticate(user=self.user)
        url = reverse(self.LIST_URL_NAME)
        response = self.client.get(url)
        response = self.client.post(url, dict(
            name='A test instrument',
            remarks="This is a test remarks.",
            thumbnail=create_dummy_image(),
        ))
        instrument = Instrument.objects.last()
        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(list(response.data.keys()), [
            'pk', 'name', 'remarks', 'thumbnail', 'owner', 'reservations',
        ])
        self.assertEqual(response.data['pk'], instrument.pk)

    def test_create_invalid(self):
        self.client.force_authenticate(user=self.user)
        url = reverse(self.LIST_URL_NAME)
        response = self.client.post(url, dict(
            remarks="This is a test remarks.",
            thumbnail=create_dummy_image(),
        ))
        self.assertEqual(response.status_code, 400, response.data)

    def test_create_anonymous(self):
        self.client.force_authenticate(user=None)
        url = reverse(self.LIST_URL_NAME)
        response = self.client.post(url, dict(
            name='A test instrument',
            remarks="This is a test remarks.",
            thumbnail=create_dummy_image(),
        ))
        self.assertEqual(response.status_code, 403, response.data)

    def test_update_valid(self):
        self.client.force_authenticate(user=self.user)
        instrument = InstrumentFactory(owner=self.user)
        url = reverse(self.DETAIL_URL_NAME, kwargs=dict(pk=instrument.pk))
        response = self.client.put(url, dict(
            name='A test instrument',
            remarks="This is a test remarks.",
            thumbnail=create_dummy_image(),
        ))
        instrument_updated = Instrument.objects.last()
        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(list(response.data.keys()), [
            'pk', 'name', 'remarks', 'thumbnail', 'owner', 'reservations',
        ])
        self.assertEqual(response.data['pk'], instrument_updated.pk)
        self.assertEqual(response.data['pk'], instrument.pk)

    def test_update_permission_denied(self):
        self.client.force_authenticate(user=self.user)
        instrument = InstrumentFactory()
        url = reverse(self.DETAIL_URL_NAME, kwargs=dict(pk=instrument.pk))
        response = self.client.put(url, dict(
            name='A test instrument',
            remarks="This is a test remarks.",
            thumbnail=create_dummy_image(),
        ))
        self.assertEqual(response.status_code, 403, response.data)

    def test_update_anonymous(self):
        self.client.force_authenticate(user=None)
        instrument = InstrumentFactory()
        url = reverse(self.DETAIL_URL_NAME, kwargs=dict(pk=instrument.pk))
        response = self.client.put(url, dict(
            name='A test instrument',
            remarks="This is a test remarks.",
            thumbnail=create_dummy_image(),
        ))
        self.assertEqual(response.status_code, 403, response.data)

    def test_delete_valid(self):
        self.client.force_authenticate(user=self.user)
        instrument = InstrumentFactory(owner=self.user)
        url = reverse(self.DETAIL_URL_NAME, kwargs=dict(pk=instrument.pk))
        n_previous = Instrument.objects.count()
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204, response.data)
        self.assertEqual(Instrument.objects.count(), n_previous - 1)

    def test_delete_permission_denied(self):
        self.client.force_authenticate(user=self.user)
        instrument = InstrumentFactory()
        url = reverse(self.DETAIL_URL_NAME, kwargs=dict(pk=instrument.pk))
        n_previous = Instrument.objects.count()
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403, response.data)
        self.assertEqual(Instrument.objects.count(), n_previous)

    def test_delete_anonymous(self):
        self.client.force_authenticate(user=None)
        instrument = InstrumentFactory()
        url = reverse(self.DETAIL_URL_NAME, kwargs=dict(pk=instrument.pk))
        n_previous = Instrument.objects.count()
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403, response.data)
        self.assertEqual(Instrument.objects.count(), n_previous)


class ReservationAPIView(TestCase):
    LIST_URL_NAME = 'reservations-api:reservations-list'
    DETAIL_URL_NAME = 'reservations-api:reservations-detail'

    def setUp(self):
        self.user = UserFactory()
        self.client = APIClient()
        self.instrument = InstrumentFactory()
        # NOTE:
        # start_at/end_at of reservation is randomly determined so remove all
        # reservations to reduce accidentaly failures
        Reservation.objects.all().delete()

    def test_list(self):
        reservations = [
            ReservationFactory(instrument=self.instrument),
            ReservationFactory(),
            ReservationFactory(instrument=self.instrument),
            ReservationFactory(),
            ReservationFactory(instrument=self.instrument),
            ReservationFactory(),
            ReservationFactory(instrument=self.instrument),
            ReservationFactory(),
            ReservationFactory(instrument=self.instrument),
            ReservationFactory(),
        ]
        url = reverse(self.LIST_URL_NAME, kwargs=dict(
            instrument_pk=self.instrument.pk,
        ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(len(response.data), 5)
        self.assertEqual(list(response.data[0].keys()), [
            'instrument', 'pk', 'name', 'contact', 'remarks',
            'start_at', 'end_at',
        ])
        self.assertEqual(
            list(sorted(map(itemgetter('pk'), response.data))),
            list(sorted(map(attrgetter('pk'), reservations[::2]))),
        )

    def test_detail(self):
        reservation = ReservationFactory(instrument=self.instrument)
        url = reverse(self.DETAIL_URL_NAME, kwargs=dict(
            instrument_pk=self.instrument.pk,
            pk=reservation.pk,
        ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(list(response.data.keys()), [
            'instrument', 'pk', 'name', 'contact', 'remarks',
            'start_at', 'end_at',
        ])
        self.assertEqual(response.data['pk'], reservation.pk)

    def test_create_valid(self):
        url = reverse(self.LIST_URL_NAME, kwargs=dict(
            instrument_pk=self.instrument.pk,
        ))
        response = self.client.post(url, dict(
            name='This is a test reservation',
            contact='Call my name with your loudest voice',
            remarks='I love dog.',
            start_at='2014-02-04T10:10:10Z',
            end_at='2014-02-04T12:10:10Z',
        ))
        reservation = Reservation.objects.last()
        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(list(response.data.keys()), [
            'instrument', 'pk', 'name', 'contact', 'remarks',
            'start_at', 'end_at', 'credential',
        ])
        self.assertEqual(response.data['pk'], reservation.pk)
        self.assertEqual(response.data['credential'],
                         str(reservation.credential))

    def test_create_invalid(self):
        url = reverse(self.LIST_URL_NAME, kwargs=dict(
            instrument_pk=self.instrument.pk,
        ))
        response = self.client.post(url, dict(
            contact='Call my name with your loudest voice',
            remarks='I love dog.',
            start_at='2014-02-04T10:10:10Z',
            end_at='2014-02-04T12:10:10Z',
        ))
        self.assertEqual(response.status_code, 400, response.data)

    def test_update_valid(self):
        reservation = ReservationFactory(
            owner=self.user,
            instrument=self.instrument,
        )
        self.client.force_authenticate(self.user)
        url = reverse(self.DETAIL_URL_NAME, kwargs=dict(
            instrument_pk=self.instrument.pk,
            pk=reservation.pk,
        ))
        response = self.client.put(url, dict(
            name='This is a test reservation',
            contact='Call my name with your loudest voice',
            remarks='I love dog.',
            start_at='2014-02-04T10:10:10Z',
            end_at='2014-02-04T12:10:10Z',
        ))
        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(list(response.data.keys()), [
            'instrument', 'pk', 'name', 'contact', 'remarks',
            'start_at', 'end_at', 'credential',
        ])
        self.assertEqual(response.data['pk'], reservation.pk)
        self.assertEqual(response.data['credential'],
                         str(reservation.credential))

    def test_update_valid_with_credential(self):
        reservation = ReservationFactory(
            instrument=self.instrument,
        )
        self.client.force_authenticate(self.user)
        self.client.credentials(**{
            'X-RESERVATION-CREDENTIAL': str(reservation.credential),
        })
        url = reverse(self.DETAIL_URL_NAME, kwargs=dict(
            instrument_pk=self.instrument.pk,
            pk=reservation.pk,
        ))
        response = self.client.put(url, dict(
            name='This is a test reservation',
            contact='Call my name with your loudest voice',
            remarks='I love dog.',
            start_at='2014-02-04T10:10:10Z',
            end_at='2014-02-04T12:10:10Z',
        ))
        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(list(response.data.keys()), [
            'instrument', 'pk', 'name', 'contact', 'remarks',
            'start_at', 'end_at', 'credential',
        ])
        self.assertEqual(response.data['pk'], reservation.pk)
        self.assertEqual(response.data['credential'],
                         str(reservation.credential))

    def test_update_valid_with_credential_anonymous(self):
        reservation = ReservationFactory(
            instrument=self.instrument,
        )
        self.client.force_authenticate(None)
        self.client.credentials(**{
            'X-RESERVATION-CREDENTIAL': str(reservation.credential),
        })
        url = reverse(self.DETAIL_URL_NAME, kwargs=dict(
            instrument_pk=self.instrument.pk,
            pk=reservation.pk,
        ))
        response = self.client.put(url, dict(
            name='This is a test reservation',
            contact='Call my name with your loudest voice',
            remarks='I love dog.',
            start_at='2014-02-04T10:10:10Z',
            end_at='2014-02-04T12:10:10Z',
        ))
        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(list(response.data.keys()), [
            'instrument', 'pk', 'name', 'contact', 'remarks',
            'start_at', 'end_at', 'credential',
        ])
        self.assertEqual(response.data['pk'], reservation.pk)
        self.assertEqual(response.data['credential'],
                         str(reservation.credential))

    def test_update_permission_denied(self):
        reservation = ReservationFactory(
            instrument=self.instrument,
        )
        self.client.force_authenticate(self.user)
        url = reverse(self.DETAIL_URL_NAME, kwargs=dict(
            instrument_pk=self.instrument.pk,
            pk=reservation.pk,
        ))
        response = self.client.put(url, dict(
            name='This is a test reservation',
            contact='Call my name with your loudest voice',
            remarks='I love dog.',
            start_at='2014-02-04T10:10:10Z',
            end_at='2014-02-04T12:10:10Z',
        ))
        self.assertEqual(response.status_code, 403, response.data)

    def test_update_permission_denied_anonymous(self):
        self.client.force_authenticate(None)
        reservation = ReservationFactory(
            instrument=self.instrument,
        )
        url = reverse(self.DETAIL_URL_NAME, kwargs=dict(
            instrument_pk=self.instrument.pk,
            pk=reservation.pk,
        ))
        response = self.client.put(url, dict(
            name='This is a test reservation',
            contact='Call my name with your loudest voice',
            remarks='I love dog.',
            start_at='2014-02-04T10:10:10Z',
            end_at='2014-02-04T12:10:10Z',
        ))
        self.assertEqual(response.status_code, 403, response.data)

    def test_update_permission_denied_with_credential(self):
        reservation = ReservationFactory(
            owner=UserFactory(),
            instrument=self.instrument,
        )
        self.client.force_authenticate(self.user)
        self.client.credentials(**{
            'X-RESERVATION-CREDENTIAL': str(reservation.credential),
        })
        url = reverse(self.DETAIL_URL_NAME, kwargs=dict(
            instrument_pk=self.instrument.pk,
            pk=reservation.pk,
        ))
        response = self.client.put(url, dict(
            name='This is a test reservation',
            contact='Call my name with your loudest voice',
            remarks='I love dog.',
            start_at='2014-02-04T10:10:10Z',
            end_at='2014-02-04T12:10:10Z',
        ))
        self.assertEqual(response.status_code, 403, response.data)

    def test_update_permission_denied_with_credential_anonymous(self):
        reservation = ReservationFactory(
            owner=UserFactory(),
            instrument=self.instrument,
        )
        self.client.force_authenticate(None)
        self.client.credentials(**{
            'X-RESERVATION-CREDENTIAL': str(reservation.credential),
        })
        url = reverse(self.DETAIL_URL_NAME, kwargs=dict(
            instrument_pk=self.instrument.pk,
            pk=reservation.pk,
        ))
        response = self.client.put(url, dict(
            name='This is a test reservation',
            contact='Call my name with your loudest voice',
            remarks='I love dog.',
            start_at='2014-02-04T10:10:10Z',
            end_at='2014-02-04T12:10:10Z',
        ))
        self.assertEqual(response.status_code, 403, response.data)

    def test_delete_valid(self):
        reservation = ReservationFactory(
            owner=self.user,
            instrument=self.instrument,
        )
        self.client.force_authenticate(self.user)
        url = reverse(self.DETAIL_URL_NAME, kwargs=dict(
            instrument_pk=self.instrument.pk,
            pk=reservation.pk,
        ))
        n_reservation = Reservation.objects.count()
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204, response.data)
        self.assertEqual(Reservation.objects.count(), n_reservation-1)

    def test_delete_valid_with_credential(self):
        reservation = ReservationFactory(
            instrument=self.instrument,
        )
        self.client.force_authenticate(None)
        self.client.credentials(**{
            'X-RESERVATION-CREDENTIAL': str(reservation.credential),
        })
        url = reverse(self.DETAIL_URL_NAME, kwargs=dict(
            instrument_pk=self.instrument.pk,
            pk=reservation.pk,
        ))
        n_reservation = Reservation.objects.count()
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204, response.data)
        self.assertEqual(Reservation.objects.count(), n_reservation-1)

    def test_delete_valid_with_credential_anonymous(self):
        reservation = ReservationFactory(
            instrument=self.instrument,
        )
        self.client.force_authenticate(self.user)
        self.client.credentials(**{
            'X-RESERVATION-CREDENTIAL': str(reservation.credential),
        })
        url = reverse(self.DETAIL_URL_NAME, kwargs=dict(
            instrument_pk=self.instrument.pk,
            pk=reservation.pk,
        ))
        n_reservation = Reservation.objects.count()
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204, response.data)
        self.assertEqual(Reservation.objects.count(), n_reservation-1)

    def test_delete_permission_denied(self):
        reservation = ReservationFactory(
            instrument=self.instrument,
        )
        self.client.force_authenticate(self.user)
        url = reverse(self.DETAIL_URL_NAME, kwargs=dict(
            instrument_pk=self.instrument.pk,
            pk=reservation.pk,
        ))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403, response.data)

    def test_delete_permission_denied_anonymous(self):
        reservation = ReservationFactory(
            instrument=self.instrument,
        )
        self.client.force_authenticate(None)
        url = reverse(self.DETAIL_URL_NAME, kwargs=dict(
            instrument_pk=self.instrument.pk,
            pk=reservation.pk,
        ))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403, response.data)

    def test_delete_permission_denied_with_credential(self):
        reservation = ReservationFactory(
            owner=UserFactory(),
            instrument=self.instrument,
        )
        self.client.force_authenticate(self.user)
        self.client.credentials(**{
            'X-RESERVATION-CREDENTIAL': str(reservation.credential),
        })
        url = reverse(self.DETAIL_URL_NAME, kwargs=dict(
            instrument_pk=self.instrument.pk,
            pk=reservation.pk,
        ))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403, response.data)

    def test_delete_permission_denied_with_credential_anonymous(self):
        reservation = ReservationFactory(
            owner=UserFactory(),
            instrument=self.instrument,
        )
        self.client.force_authenticate(None)
        self.client.credentials(**{
            'X-RESERVATION-CREDENTIAL': str(reservation.credential),
        })
        url = reverse(self.DETAIL_URL_NAME, kwargs=dict(
            instrument_pk=self.instrument.pk,
            pk=reservation.pk,
        ))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403, response.data)
