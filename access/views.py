from django.shortcuts import render

from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model

from .forms import UserAdminCreationForm

class UserCreateView(CreateView):
    model         = get_user_model()
    form_class    = UserAdminCreationForm
    template_name = 'access/new_user.html'
    success_url   = reverse_lazy('access:login')
