from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
import uuid
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.db import models
from django.utils import timezone
from datetime import timedelta
import secrets
from django.core.exceptions import ValidationError
from drf_spectacular.utils import extend_schema_field



class CustomUserManager(BaseUserManager):
    def create_user(self,email_address,password=None, **extra_fields):
        if not email_address:
            raise ValueError("The Email must be set")
        

        email_address = self.normalize_email(email_address)
        user = self.model(email_address=email_address, **extra_fields)


        user.save(using=self.__db)
        return user
    

    def create_superuser(self,email_address,pasword=None, **extra_fields):
        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_superuser",True)
        extra_fields.setdefault("provider","email")
        extra_fields.setdefault("verified_at",timezone.now())


        if not pasword:
            raise ValueError("Superuser must have a password")
        

        return self.create_user(email_address, password, **extra_fields)
    



class User(AbstractBaseUser, PermissionsMixin):

  class Role(models.TextChoices):
    ADMIN = "admin","Admin"
    LANDLORD = "landlord","Landlord"
    TENANT = "tenat","Tenant"




    id  = models.UUIDField(primary_key=True,default=uuid4, editable=False)
    role = models.CharField(max_length=20,choices=Role.choices, default=Role.TENANT)
    first