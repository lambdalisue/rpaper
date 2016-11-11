import datetime
from unittest.mock import patch
from pytz import UTC
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AnonymousUser
from .factories import (
    UserFactory,
    InstrumentFactory,
    ReservationFactory,
)
from ..models import (
    Instrument,
    Reservation,
)


class InstrumentModelTestCase(TestCase):
    def test_construction(self):
        instance = InstrumentFactory()
        instance.full_clean()
        self.assertIsInstance(instance, Instrument)

    def test_pk(self):
        i1 = InstrumentFactory()
        i2 = InstrumentFactory()
        self.assertRegex(i1.pk, r'\w{8,}')
        self.assertRegex(i2.pk, r'\w{8,}')
        self.assertNotEqual(i1.pk, i2.pk)

        i3 = InstrumentFactory.build()
        self.assertEqual(i3.pk, None)

    def test_permissions(self):
        user1 = UserFactory()
        user2 = UserFactory()
        user3 = AnonymousUser()
        instrument = InstrumentFactory(owner=user1)

        has_perm = lambda user, kind, obj=None: user.has_perm(
            "reservations.%s_instrument" % kind, obj
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

        self.assertTrue(has_perm(user1, 'change', instrument))
        self.assertFalse(has_perm(user2, 'change', instrument))
        self.assertFalse(has_perm(user3, 'change', instrument))
        self.assertTrue(has_perm(user1, 'delete', instrument))
        self.assertFalse(has_perm(user2, 'delete', instrument))
        self.assertFalse(has_perm(user3, 'delete', instrument))


class ReservationModelTestCase(TestCase):
    def test_construction(self):
        instance = ReservationFactory.build()
        self.assertIsInstance(instance, Reservation)

    def test_pk(self):
        i1 = ReservationFactory()
        i2 = ReservationFactory()
        self.assertRegex(i1.pk, r'\w{8,}')
        self.assertRegex(i2.pk, r'\w{8,}')
        self.assertNotEqual(i1.pk, i2.pk)

        i3 = ReservationFactory.build()
        self.assertEqual(i3.pk, None)

    def test_permissions(self):
        user1 = UserFactory()
        user2 = UserFactory()
        user3 = AnonymousUser()
        reservation = ReservationFactory(owner=user1)

        has_perm = lambda user, kind, obj=None: user.has_perm(
            "reservations.%s_reservation" % kind, obj
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
        # The reservation has created by an authenticated user.
        # In this case, 'credential' doesn't give any permissions.
        path = 'rpaper.apps.reservations.perms.get_reservation_credential'
        with patch(path) as get_reservation_credential:
            get_reservation_credential.return_value = None
            self.assertTrue(has_perm(user1, 'change', reservation))
            self.assertFalse(has_perm(user2, 'change', reservation))
            self.assertFalse(has_perm(user3, 'change', reservation))
            self.assertTrue(has_perm(user1, 'delete', reservation))
            self.assertFalse(has_perm(user2, 'delete', reservation))
            self.assertFalse(has_perm(user3, 'delete', reservation))

            del user1._logical_perms_cache
            del user2._logical_perms_cache
            del user3._logical_perms_cache
            get_reservation_credential.return_value = str(
                reservation.credential
            )
            self.assertTrue(has_perm(user1, 'change', reservation))
            self.assertFalse(has_perm(user2, 'change', reservation))
            self.assertFalse(has_perm(user3, 'change', reservation))
            self.assertTrue(has_perm(user1, 'delete', reservation))
            self.assertFalse(has_perm(user2, 'delete', reservation))
            self.assertFalse(has_perm(user3, 'delete', reservation))

    def test_permissions_with_credential(self):
        user1 = UserFactory()
        user2 = UserFactory()
        user3 = AnonymousUser()
        reservation = ReservationFactory()

        has_perm = lambda user, kind, obj=None: user.has_perm(
            "reservations.%s_reservation" % kind, obj
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
        # The reservation has created by an anonymous user.
        # In this case, 'credential' give permissions to user who know the
        # 'credential'.
        path = 'rpaper.apps.reservations.perms.get_reservation_credential'
        with patch(path) as get_reservation_credential:
            get_reservation_credential.return_value = None
            self.assertFalse(has_perm(user1, 'change', reservation))
            self.assertFalse(has_perm(user2, 'change', reservation))
            self.assertFalse(has_perm(user3, 'change', reservation))
            self.assertFalse(has_perm(user1, 'delete', reservation))
            self.assertFalse(has_perm(user2, 'delete', reservation))
            self.assertFalse(has_perm(user3, 'delete', reservation))

            del user1._logical_perms_cache
            del user2._logical_perms_cache
            del user3._logical_perms_cache
            get_reservation_credential.return_value = str(
                reservation.credential
            )
            self.assertTrue(has_perm(user1, 'change', reservation))
            self.assertTrue(has_perm(user2, 'change', reservation))
            self.assertTrue(has_perm(user3, 'change', reservation))
            self.assertTrue(has_perm(user1, 'delete', reservation))
            self.assertTrue(has_perm(user2, 'delete', reservation))
            self.assertTrue(has_perm(user3, 'delete', reservation))

    def test_clean_end_at_is_greater_than_start_at(self):
        instance = ReservationFactory.build(
            start_at=datetime.datetime(2014, 10, 10, 10, tzinfo=UTC),
            end_at=datetime.datetime(2014, 10, 10, 9, tzinfo=UTC),
        )
        self.assertRaises(ValidationError, instance.full_clean)

        instance = ReservationFactory.build(
            start_at=datetime.datetime(2014, 10, 10, 10, tzinfo=UTC),
            end_at=datetime.datetime(2014, 10, 10, 10, tzinfo=UTC),
        )
        self.assertRaises(ValidationError, instance.full_clean)

    def test_clean_time_span_is_greter_than_24_hours(self):
        start_at = datetime.datetime(2014, 1, 1, 0, 0, 0, tzinfo=UTC)
        instance = ReservationFactory.build(
            start_at=start_at,
            end_at=start_at+datetime.timedelta(hours=24, seconds=1),
        )
        self.assertRaises(ValidationError, instance.full_clean)

    def test_is_collided(self):
        start_at = datetime.datetime(2014, 1, 1, 12, 0, 0, tzinfo=UTC)
        end_at = start_at + datetime.timedelta(hours=1)
        reservation = ReservationFactory(
            start_at=start_at,
            end_at=end_at,
        )
        # r |------|
        # o |------|
        self.assertTrue(reservation.is_collided(ReservationFactory(
            start_at=start_at,
            end_at=end_at,
        )))
        # r |------|
        # o  |----|
        self.assertTrue(reservation.is_collided(ReservationFactory(
            start_at=start_at+datetime.timedelta(minutes=10),
            end_at=end_at-datetime.timedelta(minutes=10),
        )))
        # r  |------|
        # o |--------|
        self.assertTrue(reservation.is_collided(ReservationFactory(
            start_at=start_at-datetime.timedelta(minutes=10),
            end_at=end_at+datetime.timedelta(minutes=10),
        )))
        # r  |------|
        # o |------|
        self.assertTrue(reservation.is_collided(ReservationFactory(
            start_at=start_at-datetime.timedelta(minutes=10),
            end_at=end_at-datetime.timedelta(minutes=10),
        )))
        # r |------|
        # o  |------|
        self.assertTrue(reservation.is_collided(ReservationFactory(
            start_at=start_at+datetime.timedelta(minutes=10),
            end_at=end_at+datetime.timedelta(minutes=10),
        )))
        # r |------|
        # o        |------|
        self.assertFalse(reservation.is_collided(ReservationFactory(
            start_at=end_at,
            end_at=end_at+datetime.timedelta(hours=1),
        )))
        # r        |------|
        # o |------|
        self.assertFalse(reservation.is_collided(ReservationFactory(
            start_at=start_at-datetime.timedelta(hours=1),
            end_at=start_at,
        )))
        # r |------|
        # o         |-----|
        self.assertFalse(reservation.is_collided(ReservationFactory(
            start_at=end_at+datetime.timedelta(minutes=10),
            end_at=end_at+datetime.timedelta(hours=1),
        )))
        # r        |------|
        # o |-----|
        self.assertFalse(reservation.is_collided(ReservationFactory(
            start_at=start_at-datetime.timedelta(hours=1),
            end_at=start_at-datetime.timedelta(minutes=10),
        )))


class ReservationManagerTestCase(TestCase):
    def setUp(self):
        self.instrument = InstrumentFactory()
        self.anchor = datetime.datetime(2014, 1, 1, 12, 0, 0, tzinfo=UTC)
        d = lambda x: datetime.timedelta(hours=x)  # noqa: E731
        r = lambda s, e: ReservationFactory(  # noqa: E731
            instrument=self.instrument,
            start_at=s,
            end_at=e,
        )
        self.reservations = [
            r(self.anchor+d(i), self.anchor+d(i+1))
            for i in range(-48, 49) if i != 0
        ]

    def test__may_collide_with(self):
        # Pre registered reservations:
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
        # <reservation>
        #  +1   +2  *
        # ...
        # +22  +23  *
        # +23  +24
        # ...
        # +47  +48
        #
        reservation = ReservationFactory.build(
            instrument=self.instrument,
            start_at=self.anchor,
            end_at=self.anchor+datetime.timedelta(hours=1),
        )
        qs = Reservation.objects._may_collide_with(reservation)
        self.assertEqual(Reservation.objects.count(), 48+48)
        self.assertEqual(qs.count(), 23 + 23)

    def test_collide_with(self):
        reservation = ReservationFactory.build(
            instrument=self.instrument,
            start_at=self.anchor,
            end_at=self.anchor+datetime.timedelta(hours=1),
        )
        qs = Reservation.objects.collide_with(reservation)
        self.assertEqual(qs.count(), 0)

        reservation = ReservationFactory.build(
            instrument=self.instrument,
            start_at=self.anchor-datetime.timedelta(hours=1),
            end_at=self.anchor,
        )
        qs = Reservation.objects.collide_with(reservation)
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs.first(), self.reservations[47])

        reservation = ReservationFactory.build(
            instrument=self.instrument,
            start_at=self.anchor-datetime.timedelta(hours=2),
            end_at=self.anchor,
        )
        qs = Reservation.objects.collide_with(reservation)
        self.assertEqual(qs.count(), 2)
        self.assertQuerysetEqual(qs.all(), [
            repr(self.reservations[46]),
            repr(self.reservations[47]),
        ])
