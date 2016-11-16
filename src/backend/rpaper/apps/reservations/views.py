from django.http import Http404
from django.views.generic.base import TemplateView


class InstrumentDetailView(TemplateView):

    template_name = "reservations/instrument_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'pk' not in kwargs:
            raise Http404
        context['pk'] = kwargs['pk']
        return context
