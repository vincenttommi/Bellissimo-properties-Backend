from pathlib import Path
import os
from decouple import config
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY =  config(
    "SECRET_KEY",default="django-insecure-dtm7f9iz-r6(n!x3wnj2)+&ibbos4)e@#8x0s6iq6g5ez1yw$z")


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG",default=False, cast=bool)

ALLOWED_HOSTS = [

"localhost",
"127.0.0.1",
"178.18.243"
"0.0.0.0"

]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'drf_spectacular',
    'django_extensions',
    'users', 
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware'
]




CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000"
]

CORS_ALLOW_CREDENTIALS = True


CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

CORS_EXPOSE_HEADERS = ['set-cookie']

if DEBUG:
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False

    SESSION_COOKIE_SAMESITE = 'None'
    SESSION_COOKIE_SECURE  = True,
    SESSION_COOKIE_DOMAIN = None


ROOT_URLCONF = 'belissimo_back.urls'



REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS":"drf_spectacular.openapi.AutoSchema",
    
}



SPECTACULAR_SETTINGS = {
    'TITLE': 'Bellissimo API',
    'DESCRIPTION': '''
    *Bellissimo Backend API Documentation*
    
    Welcome to the Belissimo_backend API - a platform that connects Landlords,Tenants and those looking to buy/rent an apartment or an Airbnb, those looking to explore architectural construction projects

   
    ''',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'CONTACT': {
        'name': 'Bellissimo Support',
        'email': 'info@bellissimoproperties.co.ke',
        'url': '',
    },
    'LICENSE': {
        'name': 'Proprietary',
        'url': '',
    },
    'EXTERNAL_DOCS': {
        'description': 'Bellissimo-Properties Documentation',
        'url': 'https://tunaresq-be.tunaresq.co.ke/api/docs',
    },
    
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description': 'JWT authorization header using the Bearer scheme. Example: "Authorization: Bearer {token}"'
        }
    },
    'SECURITY': [{'Bearer': []}],
    
    # NEW: Additional Swagger UI settings for better JWT experience
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        'persistAuthorization': True,
        'displayOperationId': False,
        'defaultModelsExpandDepth': 1,
        'defaultModelExpandDepth': 1,
        'defaultModelRendering': 'example',
        'displayRequestDuration': True,
        'docExpansion': 'none',
        'filter': True,
        'operationsSorter': 'alpha',
        'showExtensions': True,
        'showCommonExtensions': True,
        'tagsSorter': 'alpha',
        'tryItOutEnabled': True,
        'validatorUrl': None,
    },
    
    # NEW: Server configuration
    'SERVERS': [
        {'url': 'http://127.0.0.1:8000', 'description': 'Development server'},
        {'url': '', 'description': 'Production server'},
    ],
}



TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'belissimo_back.wsgi.application'



EMAIL_BACKEND = config("EMAIL_BACKEND", default='django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = config("EMAIL_HOST",default='smtp.gmail.com')
EMAIL_PORT = config("EMAIL_PORT", cast=int, default=587)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", cast=bool, default=True)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="vincenttommikorir@gmail.com")
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default=EMAIL_HOST_USER)






SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME':timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME':timedelta(days=7),
    'ROTATE_REFRESH_TOKENS':True,
    'AUTH_COOKIE':'access',
    'AUTH_COOKIE_SECURE':True,
    'AUTH_COOKIE_HTTPP_ONLY':True,
    'AUTH_COOKIE_PATH': '/',
    'AUTH_COOKIE_SAMESITE':'None',
}



LOGGING = {
    "version":1,
    "disable_existing_loggers":False,
    "handlers":{
        "file":{
            "level":"DEBUG",
            "class":"logging.FileHandler",
            "filename":"debug.log",
        },
    },
    "loggers":{
        "django":{
            "handlers":["file"],
            "level":"DEBUG",
            "propagate":True,
        }
    }
}


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases



DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": config("DATABASE_NAME", default="bellissimo"),
        "USER": config("DATABASE_USERNAME", default="vincent"),
        "PASSWORD": config("DATABASE_PASSWORD", default="tommi087"),
        "HOST": config("DATABASE_HOST", default="localhost"),
        "PORT": config("DATABASE_PORT", default="5432"),
    }
}



REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSESS':[
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES':[
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PERMISSION_CLASSES':[
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS':'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE':10,
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
#Media files (User-uploaded content)


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.User'