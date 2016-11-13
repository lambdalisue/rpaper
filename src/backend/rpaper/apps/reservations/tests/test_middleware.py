from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser

from ..middleware import (
    ReservationCredentialMiddleware,
    get_reservation_credential,
)
from .factories import UserFactory


class ReservationCredentialMiddlewareTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_anonymous_user(self):
        middleware = ReservationCredentialMiddleware(lambda response: None)
        request = self.factory.get('/')
        request.user = AnonymousUser()

        middleware(request)
        self.assertEqual(get_reservation_credential(), None)

        request.META['X-RESERVATION-CREDENTIAL'] = 'foobar'
        middleware(request)
        self.assertEqual(get_reservation_credential(), 'foobar')

        del request.META['X-RESERVATION-CREDENTIAL']
        middleware(request)
        self.assertEqual(get_reservation_credential(), None)

    def test_authenticated_user(self):
        middleware = ReservationCredentialMiddleware(lambda response: None)
        request = self.factory.get('/')
        request.user = UserFactory()

        middleware(request)
        self.assertEqual(get_reservation_credential(), None)

        request.META['X-RESERVATION-CREDENTIAL'] = 'foobar'
        middleware(request)
        self.assertEqual(get_reservation_credential(), 'foobar')

        del request.META['X-RESERVATION-CREDENTIAL']
        middleware(request)
        self.assertEqual(get_reservation_credential(), None)
