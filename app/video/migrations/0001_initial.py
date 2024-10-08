# Generated by Django 5.0.9 on 2024-09-17 08:17

import django.utils.timezone
import video.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_by', models.CharField(max_length=255, verbose_name='Created By')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created Date')),
                ('updated_by', models.CharField(blank=True, max_length=255, null=True, verbose_name='Updated By')),
                ('updated_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Updated Date')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_by', models.CharField(max_length=255, verbose_name='Created By')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created Date')),
                ('updated_by', models.CharField(blank=True, max_length=255, null=True, verbose_name='Updated By')),
                ('updated_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Updated Date')),
                ('video', models.FileField(upload_to=video.models.video_file_path)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('duration', models.DurationField()),
                ('category', models.ManyToManyField(blank=True, related_name='videos_category', to='video.category')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
