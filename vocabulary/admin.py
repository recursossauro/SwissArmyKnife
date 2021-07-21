from django.contrib import admin

from .models import Language, Word, Default, Image, ImageWord

admin.site.register(Language)
admin.site.register(Word)
admin.site.register(Default)
admin.site.register(Image)
admin.site.register(ImageWord)
