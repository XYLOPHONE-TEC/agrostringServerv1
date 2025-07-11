# Generated by Django 5.2.3 on 2025-07-10 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('strings_tv', '0003_video_category_video_content_type_video_device_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='agrostringstvschedule',
            name='language',
            field=models.CharField(choices=[('en', 'English'), ('lg', 'Luganda'), ('sw', 'Swahili')], default='en', max_length=30),
        ),
        migrations.AddField(
            model_name='agrostringstvschedule',
            name='video_url',
            field=models.URLField(blank=True, help_text='YouTube/Vimeo link (optional)', null=True),
        ),
        migrations.AlterField(
            model_name='agrostringstvschedule',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='tv_videos/'),
        ),
    ]
