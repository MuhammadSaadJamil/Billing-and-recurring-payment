from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from base.models import *


class CreatePlan(CreateView):
    template_name = 'signup.html'
    model = Plan
    fields = '__all__'
    success_url = reverse_lazy('add-plan')


class ListPlan(ListView):
    template_name = 'list-plan.html'
    model = Plan
    context_object_name = 'plans'


class DetailPlan(DetailView):
    template_name = 'plan-detail.html'
    model = Plan
    context_object_name = 'plan'


class UpdatePlan(UpdateView):
    template_name = 'signup.html'
    model = Plan
    fields = '__all__'
    success_url = reverse_lazy('add-plan')


class DeletePlan(DeleteView):
    model = Plan
    success_url = '/'
