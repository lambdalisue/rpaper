from threading import local

_threadlocal = local()

HEADER_NAME = 'X-RESERVATION-CREDENTIAL'


class ReservationCredentialMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # NOTE:
        # The credential is stored in a threadlocal so each requests should
        # have a different thread-local value. But in case, the credential
        # should always be updated to prevent accidental leak.
        set_reservation_credential(request.META.get(HEADER_NAME, None))
        return self.get_response(request)


def get_reservation_credential():
    return getattr(_threadlocal, 'reservations_reservation_credential', None)


def set_reservation_credential(value):
    setattr(_threadlocal, 'reservations_reservation_credential', value)
