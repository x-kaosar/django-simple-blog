# Generated by Django 3.2.13 on 2022-06-18 12:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0012_alter_author_birthday'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='birthday',
        ),
    ]