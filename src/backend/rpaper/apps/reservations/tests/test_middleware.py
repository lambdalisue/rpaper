from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser

from ..middleware import (
    RecordCredentialMiddleware,
    get_record_credential,
)
from .factories import UserFactory


class RecordCredentialMiddlewareTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_anonymous_user(self):
        middleware = RecordCredentialMiddleware(lambda response: None)
        request = self.factory.get('/')
        request.user = AnonymousUser()

        middleware(request)
        self.assertEqual(get_record_credential(), None)

        request.META['X-RESERVATIONS-RECORD-CREDENTIAL'] = 'foobar'
        middleware(request)
        self.assertEqual(get_record_credential(), 'foobar')

        del request.META['X-RESERVATIONS-RECORD-CREDENTIAL']
        middleware(request)
        self.assertEqual(get_record_credential(), None)

    def test_authenticated_user(self):
        middleware = RecordCredentialMiddleware(lambda response: None)
        request = self.factory.get('/')
        request.user = UserFactory()

        middleware(request)
        self.assertEqual(get_record_credential(), None)

        request.META['X-RESERVATIONS-RECORD-CREDENTIAL'] = 'foobar'
        middleware(request)
        self.assertEqual(get_record_credential(), 'foobar')

        del request.META['X-RESERVATIONS-RECORD-CREDENTIAL']
        middleware(request)
        self.assertEqual(get_record_credential(), None)
