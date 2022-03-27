from django.urls import path

from .views import (
    IndexTemplateView,
    InputItemCreateView,
)



urlpatterns = [
    path('', IndexTemplateView.as_view(),name='index'),
    path('new_input_item', InputItemCreateView.as_view(),name='newInputItem'),
]
