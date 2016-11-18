from django.http import Http404
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.views.decorators.csrf import ensure_csrf_cookie


@method_decorator(ensure_csrf_cookie, 'dispatch')
class ThingDetailView(TemplateView):

    template_name = "reservations/thing_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'pk' not in kwargs:
            raise Http404
        context['pk'] = kwargs['pk']
        return context
