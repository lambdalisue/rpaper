import random
import datetime
import factory.fuzzy
from pytz import UTC
from django.contrib.auth.models import User
from ..models import (
    Instrument,
    Reservation,
)


class UserFactory(factory.DjangoModelFactory):

    class Meta:
        model = User
        django_get_or_create = ('username', 'email', 'password')

    username = factory.Faker('name')
    email = factory.Faker('email')
    password = factory.Faker('password')


class InstrumentFactory(factory.DjangoModelFactory):

    class Meta:
        model = Instrument

    name = factory.Faker('word')
    owner = factory.SubFactory(UserFactory)


class ReservationFactory(factory.DjangoModelFactory):

    class Meta:
        model = Reservation

    name = factory.Faker('name')
    contact = factory.Faker('email')
    instrument = factory.SubFactory(InstrumentFactory)

    start_at = factory.fuzzy.FuzzyDateTime(
        datetime.datetime(2008, 1, 1, tzinfo=UTC),      # type: ignore
        datetime.datetime(2008, 12, 31, tzinfo=UTC),    # type: ignore
    )

    @factory.lazy_attribute
    def end_at(self):
        delta = datetime.timedelta(
            hours=random.randint(1, 23),
        )
        return self.start_at + delta
