from django.db import models
import os
import uuid
from core.models import AuditModel


class Category(AuditModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


def video_file_path(instance, filename):
    """Generate file path for new video file"""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'videos', filename)


class Video(AuditModel):
    video_path = models.FileField(upload_to='videos/')
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    duration = models.DurationField()
    category = models.ManyToManyField(
        Category,
        related_name='videos_category',
        blank=True)

    def __str__(self):
        return self.title
