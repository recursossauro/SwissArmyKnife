from django.db import models
from django.conf import settings
from dropbox.exceptions import ApiError
import traceback
from django.contrib.auth import get_user_model

class Language (models.Model):
    name = models.CharField('name', max_length=500, unique = True)

    # Fields to backup control
    created = models.DateTimeField('Created', auto_now_add=True, null=True)
    modified = models.DateTimeField('Modified', auto_now=True, null=True)

    class Meta:
        verbose_name        = 'Language'
        verbose_name_plural = 'Languages'

    def __str__(self):
        return self.name

class Default(models.Model):

    user   = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Usuário', on_delete=models.CASCADE, unique=True)
    target_language = models.ForeignKey(Language, verbose_name='Target Language', related_name = 'target_language_id', on_delete=models.CASCADE, blank=True, null=True)
    native_language = models.ForeignKey(Language, verbose_name='Native Language', related_name = 'native_language_id', on_delete=models.CASCADE, blank=True, null=True)

    # Fields to backup control
    created = models.DateTimeField('Created', auto_now_add=True, null=True)
    modified = models.DateTimeField('Modified', auto_now=True, null=True)

    class Meta:
        verbose_name        = 'Default'
        verbose_name_plural = 'Defaults'

    def __str__(self):
        return 'Target: ' + str(self.target_language) + ' | Native: ' + str(self.native_language)

# Image shoud be Meaning
class Image (models.Model):

    user   = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Usuário', on_delete=models.CASCADE)
    image  = models.ImageField('Image', upload_to='images/', max_length=500, null=True, blank=True)

    # Fields to backup control
    created = models.DateTimeField('Created', auto_now_add=True)
    modified = models.DateTimeField('Modified', auto_now=True)

    class Meta:
        verbose_name        = 'Image'
        verbose_name_plural = 'Images'

    def get_image_url(self):
        try:
            return self.image.url
        except ValueError:
            return ""
        except ApiError as e:
            traceback.print_exc()
            return None

    def ImageWords(self):

        imageWords = ImageWord.objects.filter(user=self.user, image=self).order_by('-word__language')

        return imageWords

    def ImageTargetWords(self):

        language = Default.objects.get(user=self.user).target_language
        imageWords = ImageWord.objects.filter(user=self.user, image=self, word__language=language)

        return imageWords

    def ImageNativeWords(self):

        language = Default.objects.get(user=self.user).native_language
        imageWords = ImageWord.objects.filter(user=self.user, image=self, word__language=language)

        return imageWords

    def __str__(self):

        try:
            default = Default.objects.get(user=self.user)
            imageWords = ImageWord.objects.filter(user=self.user, image=self, word__language=default.target_language)
            result = ''
            if (len(imageWords) > 0):
                for word in imageWords:
                    if (not result == ''): result += ', '
                    result += str(word)
                return result
            else:
                imageWords = ImageWord.objects.filter(user=self.user, image=self, word__language=default.native_language)
                if (len(imageWords) > 0):
                    result = ''
                    for word in imageWords:
                        if (not result == ''): result += ', '
                        result += str(word)
                    return result
                return super(Image, self).__str__()
        except Default.DoesNotExist:
            pass

        return super(Image, self).__str__()

class Word(models.Model):
    user      = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Usuário', on_delete=models.CASCADE)
    language  = models.ForeignKey(Language, verbose_name='Language', on_delete=models.CASCADE, blank=True, null=True)
    word      = models.CharField('Word', max_length=200)

    # Fields to backup control
    created = models.DateTimeField('Created', auto_now_add=True)
    modified = models.DateTimeField('Modified', auto_now=True)

    class Meta:
        verbose_name        = 'Word'
        verbose_name_plural = 'Words'
        unique_together = ['user', 'word', 'language']

    def translations(self):
        default = Default.objects.get(user=self.user)
        imagesWords       = ImageWord.objects.filter(user = self.user, word=self)
        allImagesWords = ImageWord.objects.filter(
            user = self.user,
            image__in=models.Subquery(imagesWords.values('image'))
        )

        queryBase = Word.objects.filter(
            user=self.user,
            id__in=models.Subquery(allImagesWords.values('word_id'))
        )

        if (default.target_language==None):
            return queryBase.exclude(language = self.language)
        else:
            return queryBase.filter(language=default.native_language)


    def __str__(self):
        return self.word

class ImageWord(models.Model):
    user  = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Usuário', on_delete=models.CASCADE)
    word  = models.ForeignKey(Word, verbose_name = 'Word', on_delete=models.CASCADE)
    image = models.ForeignKey(Image, verbose_name = 'Image', on_delete=models.CASCADE)

    class Meta:
        verbose_name        = 'WordImage'
        verbose_name_plural = 'WordsImages'
        unique_together     = ['user', 'word', 'image']

    def __str__(self):
        return str(self.word)
