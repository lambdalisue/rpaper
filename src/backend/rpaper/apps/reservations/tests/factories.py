import random
import datetime
import factory.fuzzy
from pytz import UTC
from django.contrib.auth.models import User
from ..models import (
    Thing,
    Record,
)


class UserFactory(factory.DjangoModelFactory):

    class Meta:
        model = User
        django_get_or_create = ('username', 'email', 'password')

    username = factory.Faker('name')
    email = factory.Faker('email')
    password = factory.Faker('password')


class ThingFactory(factory.DjangoModelFactory):

    class Meta:
        model = Thing

    name = factory.Faker('word')
    owner = factory.SubFactory(UserFactory)


class RecordFactory(factory.DjangoModelFactory):

    class Meta:
        model = Record

    name = factory.Faker('name')
    contact = factory.Faker('email')
    thing = factory.SubFactory(ThingFactory)

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
