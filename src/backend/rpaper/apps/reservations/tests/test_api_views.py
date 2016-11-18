import datetime
from operator import itemgetter, attrgetter
from pytz import UTC
from django.test import TestCase, override_settings
from django.core.urlresolvers import reverse
from rest_framework.test import APIClient
from rpaper.core.storage.dummy import create_dummy_image
from ..models import Thing, Record
from .factories import (
    UserFactory,
    ThingFactory,
    RecordFactory,
)


@override_settings(
    DEFAULT_FILE_STORAGE='rpaper.core.storage.dummy.DummyStorage',
)
class ThingAPIView(TestCase):
    LIST_URL_NAME = 'reservations-api:things-list'
    DETAIL_URL_NAME = 'reservations-api:things-detail'

    def setUp(self):
        self.user = UserFactory()
        self.client = APIClient()

    def test_list(self):
        url = reverse(self.LIST_URL_NAME)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_detail(self):
        thing = ThingFactory()
        url = reverse(self.DETAIL_URL_NAME, kwargs=dict(pk=thing.pk))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(list(response.data.keys()), [
            'pk', 'name', 'remarks', 'thumbnail', 'owner',
        ])
        self.assertEqual(response.data['pk'], thing.pk)

    def test_create_valid(self):
        self.client.force_authenticate(user=self.user)
        url = reverse(self.LIST_URL_NAME)
        response = self.client.get(url)
        response = self.client.post(url, dict(
            name='A test thing',
            remarks="This is a test remarks.",
            thumbnail=create_dummy_image(),
        ))
        thing = Thing.objects.last()
        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(list(response.data.keys()), [
            'pk', 'name', 'remarks', 'thumbnail', 'owner',
        ])
        self.assertEqual(response.data['pk'], thing.pk)

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
            name='A test thing',
            remarks="This is a test remarks.",
            thumbnail=create_dummy_image(),
        ))
        self.assertEqual(response.status_code, 403, response.data)

    def test_update_valid(self):
        self.client.force_authenticate(user=self.user)
        thing = ThingFactory(owner=self.user)
        url = reverse(self.DETAIL_URL_NAME, kwargs=dict(pk=thing.pk))
        response = self.client.put(url, dict(
            name='A test thing',
            remarks="This is a test remarks.",
            thumbnail=create_dummy_image(),
        ))
        thing_updated = Thing.objects.last()
        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(list(response.data.keys()), [
            'pk', 'name', 'remarks', 'thumbnail', 'owner',
        ])
        self.assertEqual(response.data['pk'], thing_updated.pk)
        self.assertEqual(response.data['pk'], thing.pk)

    def test_update_permission_denied(self):
        self.client.force_authenticate(user=self.user)
        thing = ThingFactory()
        url = reverse(self.DETAIL_URL_NAME, kwargs=dict(pk=thing.pk))
        response = self.client.put(url, dict(
            name='A test thing',
            remarks="This is a test remarks.",
            thumbnail=create_dummy_image(),
        ))
        self.assertEqual(response.status_code, 403, response.data)

    def test_update_anonymous(self):
        self.client.force_authenticate(user=None)
        thing = ThingFactory()
        url = reverse(self.DETAIL_URL_NAME, kwargs=dict(pk=thing.pk))
        response = self.client.put(url, dict(
            name='A test thing',
            remarks="This is a test remarks.",
            thumbnail=create_dummy_image(),
        ))
        self.assertEqual(response.status_code, 403, response.data)

    def test_delete_valid(self):
        self.client.force_authenticate(user=self.user)
        thing = ThingFactory(owner=self.user)
        url = reverse(self.DETAIL_URL_NAME, kwargs=dict(pk=thing.pk))
        n_previous = Thing.objects.count()
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204, response.data)
        self.assertEqual(Thing.objects.count(), n_previous - 1)

    def test_delete_permission_denied(self):
        self.client.force_authenticate(user=self.user)
        thing = ThingFactory()
        url = reverse(self.DETAIL_URL_NAME, kwargs=dict(pk=thing.pk))
        n_previous = Thing.objects.count()
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403, response.data)
        self.assertEqual(Thing.objects.count(), n_previous)

    def test_delete_anonymous(self):
        self.client.force_authenticate(user=None)
        thing = ThingFactory()
        url = reverse(self.DETAIL_URL_NAME, kwargs=dict(pk=thing.pk))
        n_previous = Thing.objects.count()
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403, response.data)
        self.assertEqual(Thing.objects.count(), n_previous)


class RecordAPIView(TestCase):
    LIST_URL_NAME = 'reservations-api:records-list'
    DETAIL_URL_NAME = 'reservations-api:records-detail'

    def setUp(self):
        self.user = UserFactory()
        self.client = APIClient()
        self.thing = ThingFactory()
        # NOTE:
        # start_at/end_at of record is randomly determined so remove all
        # reservations to reduce accidentaly failures
        Record.objects.all().delete()

    def test_list(self):
        records = [
            RecordFactory(thing=self.thing),
            RecordFactory(),
            RecordFactory(thing=self.thing),
            RecordFactory(),
            RecordFactory(thing=self.thing),
            RecordFactory(),
            RecordFactory(thing=self.thing),
            RecordFactory(),
            RecordFactory(thing=self.thing),
            RecordFactory(),
        ]
        url = reverse(self.LIST_URL_NAME, kwargs=dict(
            thing_pk=self.thing.pk,
        ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(len(response.data), 5)
        self.assertEqual(list(response.data[0].keys()), [
            'thing', 'pk', 'name', 'contact', 'remarks',
            'start_at', 'end_at',
        ])
        self.assertEqual(
            list(sorted(map(itemgetter('pk'), response.data))),
            list(sorted(map(attrgetter('pk'), records[::2]))),
        )

    def test_list_filter_since(self):
        anchor = datetime.datetime(2014, 1, 1, 12, 0, 0, tzinfo=UTC)
        d = lambda x: datetime.timedelta(hours=x)  # noqa: E731
        r = lambda s, e: RecordFactory(  # noqa: E731
            thing=self.thing,
            start_at=s,
            end_at=e,
        )
        records = [
            r(anchor+d(i), anchor+d(i+1))
            for i in range(-48, 49)
        ]
        url = reverse(self.LIST_URL_NAME, kwargs=dict(
            thing_pk=self.thing.pk,
        ))
        response = self.client.get(url, dict(
            since=anchor.isoformat(),
        ))
        self.assertEqual(response.status_code, 200, response.data)
        # end_at >= anchor : anchor + 49
        self.assertEqual(len(response.data), 50)

    def test_list_filter_until(self):
        anchor = datetime.datetime(2014, 1, 1, 12, 0, 0, tzinfo=UTC)
        d = lambda x: datetime.timedelta(hours=x)  # noqa: E731
        r = lambda s, e: RecordFactory(  # noqa: E731
            thing=self.thing,
            start_at=s,
            end_at=e,
        )
        records = [
            r(anchor+d(i), anchor+d(i+1))
            for i in range(-48, 49)
        ]
        url = reverse(self.LIST_URL_NAME, kwargs=dict(
            thing_pk=self.thing.pk,
        ))
        response = self.client.get(url, dict(
            until=anchor.isoformat(),
        ))
        self.assertEqual(response.status_code, 200, response.data)
        # start_at <= anchor : anchor + 48
        self.assertEqual(len(response.data), 49)

    def test_list_filter_since_until(self):
        anchor = datetime.datetime(2014, 1, 1, 12, 0, 0, tzinfo=UTC)
        d = lambda x: datetime.timedelta(hours=x)  # noqa: E731
        r = lambda s, e: RecordFactory(  # noqa: E731
            thing=self.thing,
            start_at=s,
            end_at=e,
        )
        records = [
            r(anchor+d(i), anchor+d(i+1))
            for i in range(-48, 49)
        ]
        url = reverse(self.LIST_URL_NAME, kwargs=dict(
            thing_pk=self.thing.pk,
        ))
        response = self.client.get(url, dict(
            since=(anchor - d(5)).isoformat(),
            until=(anchor + d(5)).isoformat(),
        ))
        self.assertEqual(response.status_code, 200, response.data)
        # end_at >= anchor-5 and start_at >= anchor+5
        #  +- start_at
        #  |    +- end_at
        #  |    |   +- Should include?
        #  |    |   |
        #  v    v   v
        # -48  -47
        # ...
        #  -7   -6
        #  -6   -5  *
        # ...
        #  -1    0  *
        # <anchor>
        #  +1   +2  *
        # ...
        #  +5   +6  *
        #  +6   +7
        # ...
        # +47  +48
        #
        self.assertEqual(len(response.data), 12)

    def test_detail(self):
        record = RecordFactory(thing=self.thing)
        url = reverse(self.DETAIL_URL_NAME, kwargs=dict(
            thing_pk=self.thing.pk,
            pk=record.pk,
        ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(list(response.data.keys()), [
            'thing', 'pk', 'name', 'contact', 'remarks',
            'start_at', 'end_at',
        ])
        self.assertEqual(response.data['pk'], record.pk)

    def test_create_valid(self):
        url = reverse(self.LIST_URL_NAME, kwargs=dict(
            thing_pk=self.thing.pk,
        ))
        response = self.client.post(url, dict(
            name='This is a test record',
            contact='Call my name with your loudest voice',
            remarks='I love dog.',
            start_at='2014-02-04T10:10:10Z',
            end_at='2014-02-04T12:10:10Z',
        ))
        record = Record.objects.last()
        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(list(response.data.keys()), [
            'thing', 'pk', 'name', 'contact', 'remarks',
            'start_at', 'end_at', 'credential',
        ])
        self.assertEqual(response.data['pk'], record.pk)
        self.assertEqual(response.data['credential'],
                         str(record.credential))

    def test_create_invalid(self):
        url = reverse(self.LIST_URL_NAME, kwargs=dict(
            thing_pk=self.thing.pk,
        ))
        response = self.client.post(url, dict(
            contact='Call my name with your loudest voice',
            remarks='I love dog.',
            start_at='2014-02-04T10:10:10Z',
            end_at='2014-02-04T12:10:10Z',
        ))
        self.assertEqual(response.status_code, 400, response.data)

    def test_update_valid(self):
        record = RecordFactory(
            owner=self.user,
            thing=self.thing,
        )
        self.client.force_authenticate(self.user)
        url = reverse(self.DETAIL_URL_NAME, kwargs=dict(
            thing_pk=self.thing.pk,
            pk=record.pk,
        ))
        response = self.client.put(url, dict(
            name='This is a test record',
            contact='Call my name with your loudest voice',
            remarks='I love dog.',
            start_at='2014-02-04T10:10:10Z',
            end_at='2014-02-04T12:10:10Z',
        ))
        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(list(response.data.keys()), [
            'thing', 'pk', 'name', 'contact', 'remarks',
            'start_at', 'end_at', 'credential',
        ])
        self.assertEqual(response.data['pk'], record.pk)
        self.assertEqual(response.data['credential'],
                         str(record.credential))

    def test_update_valid_with_credential(self):
        record = RecordFactory(
            thing=self.thing,
        )
        self.client.force_authenticate(self.user)
        self.client.credentials(**{
            'X-RESERVATIONS-RECORD-CREDENTIAL': str(record.credential),
        })
        url = reverse(self.DETAIL_URL_NAME, kwargs=dict(
            thing_pk=self.thing.pk,
            pk=record.pk,
        ))
        response = self.client.put(url, dict(
            name='This is a test record',
            contact='Call my name with your loudest voice',
            remarks='I love dog.',
            start_at='2014-02-04T10:10:10Z',
            end_at='2014-02-04T12:10:10Z',
        ))
        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(list(response.data.keys()), [
            'thing', 'pk', 'name', 'contact', 'remarks',
            'start_at', 'end_at', 'credential',
        ])
        self.assertEqual(response.data['pk'], record.pk)
        self.assertEqual(response.data['credential'],
                         str(record.credential))

    def test_update_valid_with_credential_anonymous(self):
        record = RecordFactory(
            thing=self.thing,
        )
        self.client.force_authenticate(None)
        self.client.credentials(**{
            'X-RESERVATIONS-RECORD-CREDENTIAL': str(record.credential),
        })
        url = reverse(self.DETAIL_URL_NAME, kwargs=dict(
            thing_pk=self.thing.pk,
            pk=record.pk,
        ))
        response = self.client.put(url, dict(
            name='This is a test record',
            contact='Call my name with your loudest voice',
            remarks='I love dog.',
            start_at='2014-02-04T10:10:10Z',
            end_at='2014-02-04T12:10:10Z',
        ))
        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(list(response.data.keys()), [
            'thing', 'pk', 'name', 'contact', 'remarks',
            'start_at', 'end_at', 'credential',
        ])
        self.assertEqual(response.data['pk'], record.pk)
        self.assertEqual(response.data['credential'],
                         str(record.credential))

    def test_update_permission_denied(self):
        record = RecordFactory(
            thing=self.thing,
        )
        self.client.force_authenticate(self.user)
        url = reverse(self.DETAIL_URL_NAME, kwargs=dict(
            thing_pk=self.thing.pk,
            pk=record.pk,
        ))
        response = self.client.put(url, dict(
            name='This is a test record',
            contact='Call my name with your loudest voice',
            remarks='I love dog.',
            start_at='2014-02-04T10:10:10Z',
            end_at='2014-02-04T12:10:10Z',
        ))
        self.assertEqual(response.status_code, 403, response.data)

    def test_update_permission_denied_anonymous(self):
        self.client.force_authenticate(None)
        record = RecordFactory(
            thing=self.thing,
        )
        url = reverse(self.DETAIL_URL_NAME, kwargs=dict(
            thing_pk=self.thing.pk,
            pk=record.pk,
        ))
        response = self.client.put(url, dict(
            name='This is a test record',
            contact='Call my name with your loudest voice',
            remarks='I love dog.',
            start_at='2014-02-04T10:10:10Z',
            end_at='2014-02-04T12:10:10Z',
        ))
        self.assertEqual(response.status_code, 403, response.data)

    def test_update_permission_denied_with_credential(self):
        record = RecordFactory(
            owner=UserFactory(),
            thing=self.thing,
        )
        self.client.force_authenticate(self.user)
        self.client.credentials(**{
            'X-RESERVATIONS-RECORD-CREDENTIAL': str(record.credential),
        })
        url = reverse(self.DETAIL_URL_NAME, kwargs=dict(
            thing_pk=self.thing.pk,
            pk=record.pk,
        ))
        response = self.client.put(url, dict(
            name='This is a test record',
            contact='Call my name with your loudest voice',
            remarks='I love dog.',
            start_at='2014-02-04T10:10:10Z',
            end_at='2014-02-04T12:10:10Z',
        ))
        self.assertEqual(response.status_code, 403, response.data)

    def test_update_permission_denied_with_credential_anonymous(self):
        record = RecordFactory(
            owner=UserFactory(),
            thing=self.thing,
        )
        self.client.force_authenticate(None)
        self.client.credentials(**{
            'X-RESERVATIONS-RECORD-CREDENTIAL': str(record.credential),
        })
        url = reverse(self.DETAIL_URL_NAME, kwargs=dict(
            thing_pk=self.thing.pk,
            pk=record.pk,
        ))
        response = self.client.put(url, dict(
            name='This is a test record',
            contact='Call my name with your loudest voice',
            remarks='I love dog.',
            start_at='2014-02-04T10:10:10Z',
            end_at='2014-02-04T12:10:10Z',
        ))
        self.assertEqual(response.status_code, 403, response.data)

    def test_delete_valid(self):
        record = RecordFactory(
            owner=self.user,
            thing=self.thing,
        )
        self.client.force_authenticate(self.user)
        url = reverse(self.DETAIL_URL_NAME, kwargs=dict(
            thing_pk=self.thing.pk,
            pk=record.pk,
        ))
        n_record = Record.objects.count()
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204, response.data)
        self.assertEqual(Record.objects.count(), n_record-1)

    def test_delete_valid_with_credential(self):
        record = RecordFactory(
            thing=self.thing,
        )
        self.client.force_authenticate(None)
        self.client.credentials(**{
            'X-RESERVATIONS-RECORD-CREDENTIAL': str(record.credential),
        })
        url = reverse(self.DETAIL_URL_NAME, kwargs=dict(
            thing_pk=self.thing.pk,
            pk=record.pk,
        ))
        n_record = Record.objects.count()
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204, response.data)
        self.assertEqual(Record.objects.count(), n_record-1)

    def test_delete_valid_with_credential_anonymous(self):
        record = RecordFactory(
            thing=self.thing,
        )
        self.client.force_authenticate(self.user)
        self.client.credentials(**{
            'X-RESERVATIONS-RECORD-CREDENTIAL': str(record.credential),
        })
        url = reverse(self.DETAIL_URL_NAME, kwargs=dict(
            thing_pk=self.thing.pk,
            pk=record.pk,
        ))
        n_record = Record.objects.count()
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204, response.data)
        self.assertEqual(Record.objects.count(), n_record-1)

    def test_delete_permission_denied(self):
        record = RecordFactory(
            thing=self.thing,
        )
        self.client.force_authenticate(self.user)
        url = reverse(self.DETAIL_URL_NAME, kwargs=dict(
            thing_pk=self.thing.pk,
            pk=record.pk,
        ))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403, response.data)

    def test_delete_permission_denied_anonymous(self):
        record = RecordFactory(
            thing=self.thing,
        )
        self.client.force_authenticate(None)
        url = reverse(self.DETAIL_URL_NAME, kwargs=dict(
            thing_pk=self.thing.pk,
            pk=record.pk,
        ))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403, response.data)

    def test_delete_permission_denied_with_credential(self):
        record = RecordFactory(
            owner=UserFactory(),
            thing=self.thing,
        )
        self.client.force_authenticate(self.user)
        self.client.credentials(**{
            'X-RESERVATIONS-RECORD-CREDENTIAL': str(record.credential),
        })
        url = reverse(self.DETAIL_URL_NAME, kwargs=dict(
            thing_pk=self.thing.pk,
            pk=record.pk,
        ))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403, response.data)

    def test_delete_permission_denied_with_credential_anonymous(self):
        record = RecordFactory(
            owner=UserFactory(),
            thing=self.thing,
        )
        self.client.force_authenticate(None)
        self.client.credentials(**{
            'X-RESERVATIONS-RECORD-CREDENTIAL': str(record.credential),
        })
        url = reverse(self.DETAIL_URL_NAME, kwargs=dict(
            thing_pk=self.thing.pk,
            pk=record.pk,
        ))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403, response.data)
