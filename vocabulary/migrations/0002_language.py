# Generated by Django 3.2.4 on 2021-06-05 02:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vocabulary', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, unique=True, verbose_name='name')),
            ],
        ),
    ]
