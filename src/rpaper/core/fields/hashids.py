from hashids import Hashids
from django.db import models
from django.utils.translation import ugettext_lazy as _


class HashidsDescriptor:
    def __init__(self, field):
        self.field = field

    def __get__(self, instance, cls=None):
        if instance is None:
            return self
        value = instance.__dict__.get(self.field.name, None)
        return None if value is None else self.field.encode_hashids(value)

    def __set__(self, instance, value):
        # Translate hashid into an integer if necessary
        if isinstance(value, str):
            value = self.field.decode_hashids(value)
        instance.__dict__[self.field.name] = value


class HashidsField(models.BigAutoField):
    """A hashids field which use autoincrement feature of DB."""

    descriptor_class = HashidsDescriptor
    description = _(
        "Hashids which automatically generated from incremental integer."
    )

    def __init__(self,
                 hashids_salt="",
                 hashids_min_length=None,
                 *args, **kwargs):
        self.hashids_salt = hashids_salt
        self.hashids_min_length = hashids_min_length
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if self.hashids_salt != "":
            kwargs['hashids_salt'] = self.hashids_salt
        if self.hashids_min_length is not None:
            kwargs['hashids_min_length'] = self.hashids_min_length
        return name, path, args, kwargs

    def contribute_to_class(self, cls, name, **kwargs):
        super().contribute_to_class(cls, name, **kwargs)
        setattr(cls, self.name, self.descriptor_class(self))

    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return None
        elif not isinstance(value, int):
            raise AttributeError(
                "Non integer value %s is stored in db." % value,
            )
        return self.encode_hashids(value)

    def to_python(self, value):
        if value is None:
            return None
        elif isinstance(value, str):
            return value
        return self.encode_hashids(value)

    def get_prep_value(self, value):
        if not isinstance(value, str):
            raise AttributeError(
                "Unexpected value %s has specified." % value,
            )
        value = self.decode_hashids(value)
        return super().get_prep_value(value)

    def get_hashids(self):
        if not hasattr(self, '_hashids'):
            self._hashids = Hashids(
                salt=self.hashids_salt,
                min_length=self.hashids_min_length
            )
        return self._hashids

    def encode_hashids(self, value):
        hashids = self.get_hashids()
        return hashids.encode(value)

    def decode_hashids(self, value):
        hashids = self.get_hashids()
        numbers = hashids.decode(value)
        if len(numbers) != 1:
            raise AttributeError(
                "An invalid hashid %s has specified (%s)" % (
                    value, numbers,
                )
            )
        return numbers[0]
