from django.urls import path

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .views import (
    IndexTemplateView,
    WordCreateView,
    WordUpdateView,
    #VocabularyCreateView,
    VocabularyListView,
    WordWordImageCreateView,
    WordDeleteView,
    ImageCreateView,
    ImageUpdateView,
    WordListView,
)



urlpatterns = [
    path('', IndexTemplateView.as_view(),name='index'),
    path('new', WordCreateView.as_view(),name='new'),
    path('newimage', ImageCreateView.as_view(),name='newimage'),
    path('<int:pk>updateimage', ImageUpdateView.as_view(),name='updateimage'),
    path('<int:imagepk>/<slug:targetnative>/new', WordWordImageCreateView.as_view(),name='new'),
    path('<int:pk>/update', WordUpdateView.as_view(),name='update'),
    path('<int:pk>/delete', WordDeleteView.as_view(),name='delete'),

    path('vocabularylist', VocabularyListView.as_view(),name='vocabularylist'),
    path('wordlist', WordListView.as_view(),name='wordlist'),
    #path('newvocabulary', VocabularyCreateView.as_view(),name='newvocabulary'),


]
