import datetime
from unittest.mock import patch
from pytz import UTC
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AnonymousUser
from .factories import (
    UserFactory,
    ThingFactory,
    RecordFactory,
)
from ..models import (
    Thing,
    Record,
)


class ThingModelTestCase(TestCase):
    def test_construction(self):
        instance = ThingFactory()
        instance.full_clean()
        self.assertIsInstance(instance, Thing)

    def test_pk(self):
        i1 = ThingFactory()
        i2 = ThingFactory()
        self.assertRegex(i1.pk, r'\w{8,}')
        self.assertRegex(i2.pk, r'\w{8,}')
        self.assertNotEqual(i1.pk, i2.pk)

        i3 = ThingFactory.build()
        self.assertEqual(i3.pk, None)

    def test_permissions(self):
        user1 = UserFactory()
        user2 = UserFactory()
        user3 = AnonymousUser()
        thing = ThingFactory(owner=user1)

        has_perm = lambda user, kind, obj=None: user.has_perm(
            "reservations.%s_thing" % kind, obj
        )

        self.assertTrue(has_perm(user1, 'add'))
        self.assertTrue(has_perm(user2, 'add'))
        self.assertFalse(has_perm(user3, 'add'))
        self.assertTrue(has_perm(user1, 'change'))
        self.assertTrue(has_perm(user2, 'change'))
        self.assertFalse(has_perm(user3, 'change'))
        self.assertTrue(has_perm(user1, 'delete'))
        self.assertTrue(has_perm(user2, 'delete'))
        self.assertFalse(has_perm(user3, 'delete'))

        self.assertTrue(has_perm(user1, 'change', thing))
        self.assertFalse(has_perm(user2, 'change', thing))
        self.assertFalse(has_perm(user3, 'change', thing))
        self.assertTrue(has_perm(user1, 'delete', thing))
        self.assertFalse(has_perm(user2, 'delete', thing))
        self.assertFalse(has_perm(user3, 'delete', thing))


class RecordModelTestCase(TestCase):
    def test_construction(self):
        instance = RecordFactory.build()
        self.assertIsInstance(instance, Record)

    def test_pk(self):
        i1 = RecordFactory()
        i2 = RecordFactory()
        self.assertRegex(i1.pk, r'\w{8,}')
        self.assertRegex(i2.pk, r'\w{8,}')
        self.assertNotEqual(i1.pk, i2.pk)

        i3 = RecordFactory.build()
        self.assertEqual(i3.pk, None)

    def test_permissions(self):
        user1 = UserFactory()
        user2 = UserFactory()
        user3 = AnonymousUser()
        record = RecordFactory(owner=user1)

        has_perm = lambda user, kind, obj=None: user.has_perm(
            "reservations.%s_record" % kind, obj
        )

        self.assertTrue(has_perm(user1, 'add'))
        self.assertTrue(has_perm(user2, 'add'))
        self.assertTrue(has_perm(user3, 'add'))
        self.assertTrue(has_perm(user1, 'change'))
        self.assertTrue(has_perm(user2, 'change'))
        self.assertTrue(has_perm(user3, 'change'))
        self.assertTrue(has_perm(user1, 'delete'))
        self.assertTrue(has_perm(user2, 'delete'))
        self.assertTrue(has_perm(user3, 'delete'))

        # NOTE
        # The record has created by an authenticated user.
        # In this case, 'credential' doesn't give any permissions.
        path = 'rpaper.apps.reservations.perms.get_record_credential'
        with patch(path) as get_record_credential:
            get_record_credential.return_value = None
            self.assertTrue(has_perm(user1, 'change', record))
            self.assertFalse(has_perm(user2, 'change', record))
            self.assertFalse(has_perm(user3, 'change', record))
            self.assertTrue(has_perm(user1, 'delete', record))
            self.assertFalse(has_perm(user2, 'delete', record))
            self.assertFalse(has_perm(user3, 'delete', record))

            del user1._logical_perms_cache
            del user2._logical_perms_cache
            del user3._logical_perms_cache
            get_record_credential.return_value = str(
                record.credential
            )
            self.assertTrue(has_perm(user1, 'change', record))
            self.assertFalse(has_perm(user2, 'change', record))
            self.assertFalse(has_perm(user3, 'change', record))
            self.assertTrue(has_perm(user1, 'delete', record))
            self.assertFalse(has_perm(user2, 'delete', record))
            self.assertFalse(has_perm(user3, 'delete', record))

    def test_permissions_with_credential(self):
        user1 = UserFactory()
        user2 = UserFactory()
        user3 = AnonymousUser()
        record = RecordFactory()

        has_perm = lambda user, kind, obj=None: user.has_perm(
            "reservations.%s_record" % kind, obj
        )

        self.assertTrue(has_perm(user1, 'add'))
        self.assertTrue(has_perm(user2, 'add'))
        self.assertTrue(has_perm(user3, 'add'))
        self.assertTrue(has_perm(user1, 'change'))
        self.assertTrue(has_perm(user2, 'change'))
        self.assertTrue(has_perm(user3, 'change'))
        self.assertTrue(has_perm(user1, 'delete'))
        self.assertTrue(has_perm(user2, 'delete'))
        self.assertTrue(has_perm(user3, 'delete'))

        # NOTE
        # The record has created by an anonymous user.
        # In this case, 'credential' give permissions to user who know the
        # 'credential'.
        path = 'rpaper.apps.reservations.perms.get_record_credential'
        with patch(path) as get_record_credential:
            get_record_credential.return_value = None
            self.assertFalse(has_perm(user1, 'change', record))
            self.assertFalse(has_perm(user2, 'change', record))
            self.assertFalse(has_perm(user3, 'change', record))
            self.assertFalse(has_perm(user1, 'delete', record))
            self.assertFalse(has_perm(user2, 'delete', record))
            self.assertFalse(has_perm(user3, 'delete', record))

            del user1._logical_perms_cache
            del user2._logical_perms_cache
            del user3._logical_perms_cache
            get_record_credential.return_value = str(
                record.credential
            )
            self.assertTrue(has_perm(user1, 'change', record))
            self.assertTrue(has_perm(user2, 'change', record))
            self.assertTrue(has_perm(user3, 'change', record))
            self.assertTrue(has_perm(user1, 'delete', record))
            self.assertTrue(has_perm(user2, 'delete', record))
            self.assertTrue(has_perm(user3, 'delete', record))

    def test_clean_end_at_is_greater_than_start_at(self):
        instance = RecordFactory.build(
            start_at=datetime.datetime(2014, 10, 10, 10, tzinfo=UTC),
            end_at=datetime.datetime(2014, 10, 10, 9, tzinfo=UTC),
        )
        self.assertRaises(ValidationError, instance.full_clean)

        instance = RecordFactory.build(
            start_at=datetime.datetime(2014, 10, 10, 10, tzinfo=UTC),
            end_at=datetime.datetime(2014, 10, 10, 10, tzinfo=UTC),
        )
        self.assertRaises(ValidationError, instance.full_clean)

    def test_clean_time_span_is_greter_than_24_hours(self):
        start_at = datetime.datetime(2014, 1, 1, 0, 0, 0, tzinfo=UTC)
        instance = RecordFactory.build(
            start_at=start_at,
            end_at=start_at+datetime.timedelta(hours=24, seconds=1),
        )
        self.assertRaises(ValidationError, instance.full_clean)

    def test_is_collided(self):
        start_at = datetime.datetime(2014, 1, 1, 12, 0, 0, tzinfo=UTC)
        end_at = start_at + datetime.timedelta(hours=1)
        record = RecordFactory(
            start_at=start_at,
            end_at=end_at,
        )
        # r |------|
        # o |------|
        self.assertTrue(record.is_collided(RecordFactory(
            start_at=start_at,
            end_at=end_at,
        )))
        # r |------|
        # o  |----|
        self.assertTrue(record.is_collided(RecordFactory(
            start_at=start_at+datetime.timedelta(minutes=10),
            end_at=end_at-datetime.timedelta(minutes=10),
        )))
        # r  |------|
        # o |--------|
        self.assertTrue(record.is_collided(RecordFactory(
            start_at=start_at-datetime.timedelta(minutes=10),
            end_at=end_at+datetime.timedelta(minutes=10),
        )))
        # r  |------|
        # o |------|
        self.assertTrue(record.is_collided(RecordFactory(
            start_at=start_at-datetime.timedelta(minutes=10),
            end_at=end_at-datetime.timedelta(minutes=10),
        )))
        # r |------|
        # o  |------|
        self.assertTrue(record.is_collided(RecordFactory(
            start_at=start_at+datetime.timedelta(minutes=10),
            end_at=end_at+datetime.timedelta(minutes=10),
        )))
        # r |------|
        # o        |------|
        self.assertFalse(record.is_collided(RecordFactory(
            start_at=end_at,
            end_at=end_at+datetime.timedelta(hours=1),
        )))
        # r        |------|
        # o |------|
        self.assertFalse(record.is_collided(RecordFactory(
            start_at=start_at-datetime.timedelta(hours=1),
            end_at=start_at,
        )))
        # r |------|
        # o         |-----|
        self.assertFalse(record.is_collided(RecordFactory(
            start_at=end_at+datetime.timedelta(minutes=10),
            end_at=end_at+datetime.timedelta(hours=1),
        )))
        # r        |------|
        # o |-----|
        self.assertFalse(record.is_collided(RecordFactory(
            start_at=start_at-datetime.timedelta(hours=1),
            end_at=start_at-datetime.timedelta(minutes=10),
        )))


class RecordManagerTestCase(TestCase):
    def setUp(self):
        self.thing = ThingFactory()
        self.anchor = datetime.datetime(2014, 1, 1, 12, 0, 0, tzinfo=UTC)
        d = lambda x: datetime.timedelta(hours=x)  # noqa: E731
        r = lambda s, e: RecordFactory(  # noqa: E731
            thing=self.thing,
            start_at=s,
            end_at=e,
        )
        self.records = [
            r(self.anchor+d(i), self.anchor+d(i+1))
            for i in range(-48, 49) if i != 0
        ]

    def test__may_collide_with(self):
        # Pre registered records:
        #
        #  +- start_at
        #  |    +- end_at
        #  |    |   +- Should include?
        #  |    |   |
        #  v    v   v
        # -48  -47
        # ...
        # -24  -23
        # -23  -22  *
        # ...
        #  -1    0  *
        # <record>
        #  +1   +2  *
        # ...
        # +22  +23  *
        # +23  +24
        # ...
        # +47  +48
        #
        record = RecordFactory.build(
            thing=self.thing,
            start_at=self.anchor,
            end_at=self.anchor+datetime.timedelta(hours=1),
        )
        qs = Record.objects._may_collide_with(record)
        self.assertEqual(Record.objects.count(), 48+48)
        self.assertEqual(qs.count(), 23 + 23)

    def test_collide_with(self):
        record = RecordFactory.build(
            thing=self.thing,
            start_at=self.anchor,
            end_at=self.anchor+datetime.timedelta(hours=1),
        )
        qs = Record.objects.collide_with(record)
        self.assertEqual(qs.count(), 0)

        record = RecordFactory.build(
            thing=self.thing,
            start_at=self.anchor-datetime.timedelta(hours=1),
            end_at=self.anchor,
        )
        qs = Record.objects.collide_with(record)
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs.first(), self.records[47])

        record = RecordFactory.build(
            thing=self.thing,
            start_at=self.anchor-datetime.timedelta(hours=2),
            end_at=self.anchor,
        )
        qs = Record.objects.collide_with(record)
        self.assertEqual(qs.count(), 2)
        self.assertQuerysetEqual(qs.all(), [
            repr(self.records[46]),
            repr(self.records[47]),
        ])
