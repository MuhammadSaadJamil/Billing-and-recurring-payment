from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from base.models import *
from usage.utils import get_object_by_id


class CreateFeature(CreateView):
    template_name = 'admin_templates/add-form.html'
    model = Feature
    fields = '__all__'
    success_url = reverse_lazy('list-feature')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Feature'
        context['heading'] = 'Add Feature'
        context['features_active'] = 'active'
        context['button_text'] = 'Add Feature'
        return context


class ListFeature(ListView):
    template_name = 'admin_templates/list-features.html'
    model = Feature
    context_object_name = 'features'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Features'
        context['heading'] = 'Features'
        context['button'] = 'Add +'
        context['link'] = reverse('add-feature')
        context['features_active'] = 'active'
        return context


class DetailFeature(DetailView):
    template_name = 'admin_templates/feature.html'
    model = Feature
    context_object_name = 'feature'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Feature Details'
        context['heading'] = 'Feature Details'
        context['features_active'] = 'active'
        context['button'] = 'Edit'
        context['link'] = reverse('update-feature', args=[self.object.id])
        return context

    def get(self, request, *args, **kwargs):
        if not get_object_by_id(self.model, kwargs['pk']):
            return render(request, 'error/404_err.html', {'data': 'Plan'})
        return super().get(request, *args, **kwargs)


class UpdateFeature(UpdateView):
    template_name = 'admin_templates/add-form.html'
    model = Feature
    fields = '__all__'
    success_url = reverse_lazy('list-feature')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Feature'
        context['heading'] = 'Update Feature'
        context['features_active'] = 'active'
        context['button_text'] = 'Update Feature'
        return context


class DeleteFeature(DeleteView):
    template_name = 'admin_templates/delete.html'
    model = Feature
    success_url = reverse_lazy('list-feature')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Feature'
        context['heading'] = 'Delete Feature'
        context['features_active'] = 'active'
        return context
