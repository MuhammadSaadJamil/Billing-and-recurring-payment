from django.views.generic import DetailView

from base.models import Feature


class DetailFeature(DetailView):
    template_name = 'buyer/feature.html'
    model = Feature
    context_object_name = 'feature'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Feature Details'
        context['heading'] = 'Feature Details'
        return context
