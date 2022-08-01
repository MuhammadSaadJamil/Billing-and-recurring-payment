from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from base.models import *


class CreatePlan(CreateView):
    template_name = 'admin_templates/add-form.html'
    model = Plan
    fields = '__all__'
    success_url = reverse_lazy('list-plan')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Plans'
        context['heading'] = 'Add Plans'
        context['plans_active'] = 'active'
        context['button_text'] = 'Add Plan'
        return context


class ListPlan(ListView):
    template_name = 'admin_templates/list-plans.html'
    model = Plan
    context_object_name = 'plans'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Plans'
        context['heading'] = 'Plans'
        context['button'] = 'Add +'
        context['link'] = reverse('add-plan')
        context['plans_active'] = 'active'
        return context


class DetailPlan(DetailView):
    template_name = 'admin_templates/plan.html'
    model = Plan
    context_object_name = 'plan'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Plan Details'
        context['heading'] = 'Plan Details'
        context['plans_active'] = 'active'
        context['button'] = 'Edit'
        context['link'] = reverse('update-plan', args=[self.object.id])
        return context


class UpdatePlan(UpdateView):
    template_name = 'admin_templates/add-form.html'
    model = Plan
    fields = '__all__'
    success_url = reverse_lazy('list-plan')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Plan'
        context['heading'] = 'Update Plan'
        context['plans_active'] = 'active'
        context['button_text'] = 'Update Plan'
        return context


class DeletePlan(DeleteView):
    template_name = 'admin_templates/delete.html'
    model = Plan
    success_url = reverse_lazy('list-plan')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Plan'
        context['heading'] = 'Delete Plan'
        context['plans_active'] = 'active'
        return context
