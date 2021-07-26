# -*- coding: utf-8 -*-

from django.contrib.auth.forms import UserCreationForm
from django import forms

from django.contrib.auth import get_user_model


User = get_user_model()


class UserAdminCreationForm(UserCreationForm):

    class Meta:
            model = User
            fields = ['username', 'email']

class UserAdminForm(forms.ModelForm):

    class Meta:
            model = User
            fields = ['username', 'email', 'is_active', 'is_staff']
