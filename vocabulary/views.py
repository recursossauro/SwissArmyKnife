from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from django.db import transaction

from django.views.generic.base import View
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse

from dropbox.exceptions import ApiError
import traceback


from .models import Word, Language, Default, Image, ImageWord

class VocabularyBase():

    def loadBase(self, request):

        if (not hasattr(self, 'default') or not hasattr(self, 'nativeWords') or not hasattr(self, 'targetWords')):
            self.default = Default.objects.get(user = self.request.user)
            self.nativeWords = Word.objects.filter(user = self.request.user, language = self.default.native_language)
            self.targetWords = Word.objects.filter(user = self.request.user, language = self.default.target_language)

    def setDefaultContext(self, request, context):


        self.loadBase(request);

        context['default']     = self.default
        context['nativeWords'] = self.nativeWords
        context['targetWords'] = self.targetWords

        return context;

class IndexTemplateView(LoginRequiredMixin, TemplateView, VocabularyBase):

    template_name = 'vocabulary/index.html'

    def get_context_data(self, **kwargs):

        return self.setDefaultContext(self.request, super(self.__class__, self).get_context_data(**kwargs))

class WordCreateView(LoginRequiredMixin, CreateView, VocabularyBase):

    template_name = 'vocabulary/new.html'
    model         = Word
    fields        = ['language', 'word', 'article', 'sentence']
    success_url   = reverse_lazy('vocabulary:vocabularylist')


    def form_valid(self, form):

        form.instance.user = self.request.user

        return super(WordCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):

        return self.setDefaultContext(self.request, super(self.__class__, self).get_context_data(**kwargs))

class WordDeleteView(LoginRequiredMixin, DeleteView, VocabularyBase):

    template_name = 'vocabulary/confirm_delete.html'
    model         = Word
    success_url   = reverse_lazy('vocabulary:vocabularylist')

    def get_context_data(self, **kwargs):

        return self.setDefaultContext(self.request, super(self.__class__, self).get_context_data(**kwargs))

class WordWordImageCreateView(LoginRequiredMixin, CreateView, VocabularyBase):

    template_name = 'vocabulary/new.html'
    model         = Word
    fields        = ['word', 'article','sentence']
    success_url   = reverse_lazy('vocabulary:vocabularylist')


    def form_valid(self, form):

        self.loadBase(self.request)
        form.instance.user     = self.request.user
        form.instance.language = self.default.target_language
        if (self.kwargs['targetnative']=='native'): form.instance.language = self.default.native_language


        try:
            result = super(self.__class__, self).form_valid(form)
            imageWord = ImageWord(user=self.request.user, image=get_object_or_404(Image, pk=self.kwargs['imagepk']), word=form.instance).save()
        except IntegrityError as e:

            imageWord = ImageWord(
                user=self.request.user,
                image=get_object_or_404(Image, user=self.request.user, pk=self.kwargs['imagepk']),
                word=get_object_or_404(Word, user=self.request.user, word=form.instance.word, language=form.instance.language)
            ).save()
            result = HttpResponseRedirect(reverse('vocabulary:vocabularylist'))
            #result = HttpResponseRedirect(self.get_success_url())

        return result

    def get_context_data(self, **kwargs):

        context = self.setDefaultContext(self.request, super(self.__class__, self).get_context_data(**kwargs))
        context['image'] = get_object_or_404(Image, pk=self.kwargs['imagepk'])

        if ('targetnative' in self.kwargs and self.kwargs['targetnative']=='target'):
            context['language'] = self.default.target_language
        else:
            context['language'] = self.default.native_language

        return context

class WordUpdateView(LoginRequiredMixin, UpdateView, VocabularyBase):

    template_name = 'vocabulary/new.html'
    model         = Word
    fields        = ['language', 'word']
    success_url   = reverse_lazy('vocabulary:vocabularylist')

    def form_valid(self, form):

        form.instance.user = self.request.user

        return super(WordUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):

        return self.setDefaultContext(self.request, super(self.__class__, self).get_context_data(**kwargs))

class VocabularyCreateView(LoginRequiredMixin, CreateView, VocabularyBase):

    template_name = 'vocabulary/new_vocabulary.html'
    model         = Word
    fields        = ['word']
    success_url   = reverse_lazy('vocabulary:index')

    def form_valid(self, form):

        form.instance.user     = self.request.user

        self.loadBase(request);
        form.instance.language = self.targetWords

        return super(WordUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):

        return self.setDefaultContext(self.request, super(self.__class__, self).get_context_data(**kwargs))

class ImageCreateView(LoginRequiredMixin, CreateView, VocabularyBase):

    template_name = 'vocabulary/new.html'
    model         = Image
    fields        = ['image']
    success_url   = reverse_lazy('vocabulary:vocabularylist')


    def form_valid(self, form):

        form.instance.user = self.request.user

        return super(ImageCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):

        return self.setDefaultContext(self.request, super(self.__class__, self).get_context_data(**kwargs))

class ImageUpdateView(LoginRequiredMixin, UpdateView, VocabularyBase):

    template_name = 'vocabulary/new.html'
    model         = Image
    fields        = ['image']
    success_url   = reverse_lazy('vocabulary:vocabularylist')

    def get_object(self):

        image = get_object_or_404(Image, user=self.request.user, pk = self.kwargs['pk'])
        if (image.image != None):
            try:
                image.image.url
            except ApiError as e:
                traceback.print_exc()
                image.image = None
            except ValueError as e:
                # Prevent master.image == None
                pass

        return image


    def get_context_data(self, **kwargs):

        return self.setDefaultContext(self.request, super(self.__class__, self).get_context_data(**kwargs))

class VocabularyListView(LoginRequiredMixin, ListView, VocabularyBase):

    template_name = 'vocabulary/vocabulary_list.html'

    def get_queryset(self):

        self.loadBase(self.request)
        queryset = Image.objects.filter(user = self.request.user)

        return queryset

    def get_context_data(self, **kwargs):

        context = self.setDefaultContext(self.request, super(self.__class__, self).get_context_data(**kwargs))

        return context

class WordListView(LoginRequiredMixin, ListView, VocabularyBase):

    template_name = 'vocabulary/word_list.html'

    def get_queryset(self):

        self.loadBase(self.request)
        queryset = self.targetWords

        return queryset

    def get_context_data(self, **kwargs):

        context = self.setDefaultContext(self.request, super(self.__class__, self).get_context_data(**kwargs))

        return context
