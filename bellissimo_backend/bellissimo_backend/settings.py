import os 
from pathlib import Path
from logging import config
from decouple import confiig

from  datetime import timedelta
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config(
"SECRET_KEY", default='django-insecure-q-nwq%@wqx&@2l8_9xb+!g09j-19&-)%n7wnb^d91g(@@4po^$'
)
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = [

    "localhost",
    #Allows requests using http://localhost:... (common for local development).
    "127.0.0.1",
    #Allows requests via the IPv4 loopback address.
    "0.0.0.0"
    "178.18.243.142",
    #Allows direct access to your app via that public IP.
]


EMAIL_BACKEND = config('EMAIL_BACKEND', default="django.core.mail.backends.smtp.EmailBackend")
EMAIL_BACKEND = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT',cast=int, default=True)
EMAIL_HOST_TLS = config('EMAIL_USE_TLS', cast=bool, default=True)
EMAIL_HOST_USER = config('EMAIL_HOST_USER',defaul='vincenttommikorir@gmail.com' )
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')

DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL',default=EMAIL_HOST_USER)
# Application definition


#logging.basicConfig(level=logging.DEBUG)
#logging is configured to log debug messages to a file named  'debug.log'
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": "debug.log",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django-extensions',
    'rest_framework',
    'rest_framework_simplejwt',
    'corheaders',
    'drf_spectacular',
    'django_filters'

    

]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware'
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]



CORS_ALLOW_CREDENTIALS = True


CORS_ALLOW_ORIGINS = [
    "http://localhost:3000",   
]

CORS_ALLOW_HEADERS  = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]
CORS_ALLOW_HEADERS = ['set_cookie']  # optional for debugging


if DEBUG:
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE  = False


    SESSION_COOKIE_SAMESITE = 'None'
    SESSION_COOKIE_SECURE  = True
    SESSION_COOKIE_DOMAIN  = None



    SESSION_COOKIE_SAMESITE = 'None'
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_DOMAIN = None



REST_FRAMEWORK = {
    

    "DEFAULT_SCHEMA_CLASS":"drf_spectacular.openapi.AutoSchema",



}
    







AUTH_USER_MODEL  = 'user.User'


ROOT_URLCONF = 'bellissimo_backend.urls'



SPECTACULAR_SETTINGS = {
    'TITLE': 'Bellissimo Properties',
    'DESCRIPTION': '''
    *Bellissimo Properties API Documentation*
    
    Welcome to the Bellissimo Properties  - a platform that  enables landlord, tenant ad house buyers to interact seamlessly.
   
    ''',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'CONTACT': {
        'name': 'Bellissimo Properties Support',
        'email': 'vincenttommikorir@gmail.com',
        'url': '',
    },
    'LICENSE': {
        'name': 'Proprietary',
        'url': '',
    },
    'EXTERNAL_DOCS': {
        'description': 'Bellissimo Properties Documentation',
        'url': '',
    },
    
    # NEW: JWT Authentication Configuration for Swagger
    'AUTHENTICATION_WHITELIST': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
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
        'persistAuthorization': True,  # Keep authorization after page refresh
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



SIMPLE_JWT  = {
    'ACCESS_TOKEN_LIFETIME':timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME':timedelta(days=7),
    'ROTATE_REFRESH_TOKENS':True,
    'BLACKLIST_AFTER_ROTATION':True,
    'AUTH_COOKIE':'access',
    'AUTH_COOKIE_SECURE':True,
    'AUTH_COOKIE_HTTP_ONLY':True,
    'AUTH_COOKIE_PATH':'/',
    'AUTH_COOKIE_SAMESITE':'None'
}



TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'bellissimo_backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycop2',
        'NAME': config("DB_NAME", default="tunaresq_db"),
        "USER": config("DB_USER",default="tunaresq_user"),
        "PASSWORD":config("DB_PASSWORD",default=""),
        "HOST":config("DB_HOST",default="localhost"),
        "PORT":config("DB_PORT", default="5432"),
    },
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path(BASE_DIR, "staticfiles")
#Media files (User-uploaded content)
MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


APPEND_SLASH = False




LOGGING =  {
    "version":1,
    "disable_existing_loggers":False,
    "handlers":{
        "file":{
            "level": "DEBUG",
            "class":"logging.FileHandler",
            "filename":"debug.log",

        },
    },
    "loggers":{
        "django":{
            "handlers":["file"],
            "level":"DEDUG",
            "propagat":True,
        },
    },
}