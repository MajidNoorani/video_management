# Generated by Django 5.0.9 on 2024-09-16 10:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='video',
            old_name='video_path',
            new_name='video',
        ),
    ]
