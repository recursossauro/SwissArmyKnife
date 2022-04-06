from django.db import models
from django.conf import settings
from django.utils.timezone import now


class Input_item(models.Model):

    user        = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Usuário', on_delete=models.CASCADE)
    date        = models.DateTimeField('Data', default=now, blank=True)
    description = models.TextField('Description', max_length=100000, null=True, blank=True)
    processed   = models.BooleanField('Processed', default=False)
    inactive    = models.BooleanField('Inactive', default=False)

    # Fields to backup control
    created = models.DateTimeField('Created', auto_now_add=True, null=True)
    modified = models.DateTimeField('Modified', auto_now=True, null=True)

    class Meta:
        verbose_name        = 'Input_item'
        verbose_name_plural = 'Input_items'
        ordering            = ['date']

    def __str__(self):

        return str(self.date) + ' - ' + self.description
