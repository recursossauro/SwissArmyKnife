from django.urls import path

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .views import IndexTemplateView


urlpatterns = [
    path('', IndexTemplateView.as_view(),name='index'),
]
