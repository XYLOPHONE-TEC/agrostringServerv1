# Generated by Django 5.2.3 on 2025-07-06 19:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('strings_tv', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='category',
        ),
    ]
