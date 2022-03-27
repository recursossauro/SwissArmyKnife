from django.shortcuts import render

from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse

from dropbox.exceptions import ApiError

class IndexTemplateView(LoginRequiredMixin, TemplateView):

    template_name = 'gtd/index.html'
