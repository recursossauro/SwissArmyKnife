from django.shortcuts import render

from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse

from .models import Input_item

from dropbox.exceptions import ApiError

class IndexTemplateView(LoginRequiredMixin, TemplateView):

    template_name = 'gtd/index.html'

class InputItemCreateView(LoginRequiredMixin, CreateView):

    template_name = 'gtd/new_input_item.html'
    model = Input_item
    fields = ['date', 'description']
    success_url   = reverse_lazy('gtd:newInputItem')

    def form_valid(self, form):

        form.instance.user = self.request.user

        return super(InputItemCreateView, self).form_valid(form)
