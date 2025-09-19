from django.db import models

class SoftDeleteManager(Models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)
    