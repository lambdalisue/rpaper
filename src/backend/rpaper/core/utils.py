from functools import wraps


def validate_on_save(klass):
    original_save = klass.save

    def wrapper(self, *args, **kwargs):
        klass.full_clean(self)
        return original_save(self, *args, **kwargs)
    setattr(klass, 'save', wraps(original_save)(wrapper))
    return klass


# http://stackoverflow.com/questions/4581789/how-do-i-get-user-ip-address-in-django
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
