from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from base.models import *


class CreateFeature(CreateView):
    template_name = 'signup.html'
    model = Feature
    fields = '__all__'
    success_url = reverse_lazy('add-plan')


class ListFeature(ListView):
    model = Feature
    context_object_name = 'features'


class DetailFeature(DetailView):
    model = Feature
    context_object_name = 'feature'


class UpdateFeature(UpdateView):
    model = Feature
    fields = '__all__'
    success_url = reverse_lazy('add-plan')


class DeleteFeature(DeleteView):
    model = Feature
    success_url = '/'
