# Generated by Django 3.2.4 on 2022-03-27 17:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gtd', '0003_rename_descricao_input_item_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='input_item',
            old_name='Description',
            new_name='description',
        ),
    ]
