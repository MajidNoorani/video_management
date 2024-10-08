"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 5.0.9.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
# from dotenv import load_dotenv
from dotenv import dotenv_values
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# load envitornment variables
# load_dotenv(os.path.join(BASE_DIR.parent, '.env'))
config = dotenv_values(os.path.join(BASE_DIR.parent, '.env'))
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config['DJANGO_SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config["DEBUG"].lower() in ('true', '1', 't', 'True') or False

ALLOWED_HOSTS = []
ALLOWED_HOSTS.extend(
    filter(
        None,
        config['ALLOWED_HOSTS'].split(','),
    )
)

CORS_ALLOWED_ORIGINS = config["CORS_ALLOWED_ORIGINS"].split(',') or 'http://localhost:3000'
CORS_ALLOW_CREDENTIALS = True
# CORS_ALLOW_HEADERS = ['*']
CSRF_TRUSTED_ORIGINS = config["CORS_ALLOWED_ORIGINS"].split(',') or 'http://localhost:3000'

# Application definition

INSTALLED_APPS = [
    'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'drf_spectacular',
    'app',
    'video',
    'keycloakAuth.keycloakAuth',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': config['DB_HOST'] or '127.0.0.1',
        'NAME': config['DB_NAME'] or 'videoManagement',
        'USER': config['DB_USER'] or 'devuser',
        'PASSWORD': config['DB_PASS'] or 'changeme'
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_L10N = True

USE_TZ = True


REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'keycloakAuth.keycloakAuth.authentication.KeycloakAuthentication',
    ],
    'DEFAULT_PARSER_CLASSES': [
       'rest_framework.parsers.FormParser',
       'rest_framework.parsers.MultiPartParser',
       'rest_framework.parsers.JSONParser',
    ],
    'DEFAULT_PAGINATION_CLASS': 'core.pagination.CustomPageNumberPagination',
    'PAGE_SIZE': 12,
    'EXCEPTION_HANDLER': 'core.exceptions.custom_exception_handler'
}

AUTHENTICATION_BACKENDS = [
    'keycloakAuth.keycloakAuth.backend.KeycloakBackend',
    'django.contrib.auth.backends.ModelBackend',
]



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/static/'
MEDIA_URL = 'static/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'vol/web/media')
STATIC_ROOT = os.path.join(BASE_DIR, 'vol/web/static')


STATICFILES_DIRS = [os.path.join(BASE_DIR, STATIC_URL)]

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


SPECTACULAR_SETTINGS = {
    'TITLE': 'Video Management APIs',
    'DESCRIPTION': 'API documentation for Video Management',
    'VERSION': '1.0.0',
    'COMPONENT_SPLIT_REQUEST': True,
    'SCHEMA_PATH_PREFIX': '/api/',
    'SECURITY': [{'BearerAuth': []}],
    'AUTHENTICATION': [
        'keycloakAuth.authentication.KeycloakAuthenticationScheme',
    ],
}


# Add the ASGI application
ASGI_APPLICATION = "app.asgi.application"

# Configure channel layers
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}


# Keycloak env variables

KEYCLOAK_SERVER_URL = config["KEYCLOAK_SERVER_URL"] or 'https://keycloak.com'
KEYCLOAK_REALM = config["KEYCLOAK_REALM"] or 'VideoManagement'
KEYCLOAK_CLIENT_ID = config["KEYCLOAK_CLIENT_ID"] or 'ClientID'
KEYCLOAK_CLIENT_SECRET = config["KEYCLOAK_CLIENT_SECRET"] or 'changeme'
KEYCLOAK_REDIRECT_URI = config["KEYCLOAK_REDIRECT_URI"] or 'http://localhost:8000/api/keycloakAuth/callback/'
KEYCLOAK_ADMIN = config["KEYCLOAK_ADMIN"] or 'admin'
KEYCLOAK_ADMIN_PASSWORD = config["KEYCLOAK_ADMIN_PASSWORD"] or 'changeme'
FRONT_URL = config["FRONT_URL"] or "https://example.com"  # front url of the project
BACKEND_URL = config["BACKEND_URL"] or "http://localhost:8000"  # backend url of the project
BASE_FRONTEND_URL = config["BASE_FRONTEND_URL"] or "http://localhost:8000"

DATA_UPLOAD_MAX_NUMBER_FIELDS = 1073741824
FILE_UPLOAD_MAX_MEMORY_SIZE = 1073741824  # 1GB
DATA_UPLOAD_MAX_MEMORY_SIZE = 1073741824  # 1GB

FILE_UPLOAD_HANDLERS = [
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
    'django.core.files.uploadhandler.MemoryFileUploadHandler',
]


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'channels': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}