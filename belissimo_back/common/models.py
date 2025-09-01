from django.utils import timezone
from django.db import models
from ..common.managers import SoftDeleteManager
import uuid
from django.utils.text import slugify
from django.conf import settings


# TODO DEPRECATION NOTICE (2025.06.21) - To avoid circular imports we import settings which is 'user.User'
# User = get_user_model()


#TimeStampedModel for common timestamp fields
class TimeStampedModel(models.Model):
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL,related_name='+')
    deleted_at = models.DateTimeField(null=True,blank=True)

    class Meta:
        abstract = True



#SoftDeletableModel for softt deletion functionality
class SoftDeleteModel(TimeStampedModel):
    objects = SoftDeleteManager()  #Default manager excludes deleted
    all_objects = models.Manager() # use this to include deleted records when needed
    class Meta:
        abstract = True

    def soft_delete(self,user=None):
        self.deleted_at = timezone.now()  
        if user:
            self.deleted_by = user
            self.save()



       