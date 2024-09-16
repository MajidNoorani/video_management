
from django.db import models
from django.utils import timezone


class AuditModel(models.Model):
    created_by = models.CharField(
        max_length=255,
        verbose_name="Created By"
        )
    created_date = models.DateTimeField(
        default=timezone.now,
        verbose_name="Created Date"
        )
    updated_by = models.CharField(
        max_length=255,
        verbose_name="Updated By",
        null=True,
        blank=True
        )
    updated_date = models.DateTimeField(
        default=timezone.now,
        verbose_name="Updated Date"
        )

    class Meta:
        abstract = True
