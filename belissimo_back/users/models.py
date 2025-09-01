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



