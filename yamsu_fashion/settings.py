"""
Django settings for yamsu_fashion project.
"""

import os
from pathlib import Path
from urllib.parse import urlparse


BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY

SECRET_KEY = 'django-insecure-89)))k7x_n-3@$f41a#6e(&t#pq!=t(kmp2f#dn@j0l+)egn)@'

DEBUG = True

ALLOWED_HOSTS = ['*']


# APPLICATIONS

INSTALLED_APPS = [

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Cloudinary (gardé pour plus tard)
    'cloudinary',
    'cloudinary_storage',

    # Application boutique
    'shop',

]


# MIDDLEWARE

MIDDLEWARE = [

    'django.middleware.security.SecurityMiddleware',

    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.common.CommonMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',

    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]


# URL CONFIGURATION

ROOT_URLCONF = 'yamsu_fashion.urls'


# TEMPLATES

TEMPLATES = [

    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        'DIRS': [],

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


# WSGI

WSGI_APPLICATION = 'yamsu_fashion.wsgi.application'


# DATABASE

DATABASES = {

    'default': {

        'ENGINE': 'django.db.backends.sqlite3',

        'NAME': BASE_DIR / 'db.sqlite3',

    }

}


# PASSWORD VALIDATION

AUTH_PASSWORD_VALIDATORS = [

    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },

    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },

    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },

    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },

]


# LANGUAGE

LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'Africa/Lagos'

USE_I18N = True

USE_TZ = True


# STATIC FILES

STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / 'staticfiles'


# MEDIA FILES (images produits)

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'


# CLOUDINARY CONFIGURATION

CLOUDINARY_URL = os.getenv('CLOUDINARY_URL')

if CLOUDINARY_URL:
    cloudinary_url = urlparse(CLOUDINARY_URL)
    CLOUDINARY_STORAGE = {
        'CLOUD_NAME': cloudinary_url.hostname,
        'API_KEY': cloudinary_url.username,
        'API_SECRET': cloudinary_url.password,
    }
else:
    CLOUDINARY_STORAGE = {
        'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
        'API_KEY': os.getenv('CLOUDINARY_API_KEY'),
        'API_SECRET': os.getenv('CLOUDINARY_API_SECRET'),
    }

cloudinary_enabled = all(CLOUDINARY_STORAGE.values())


# STORAGE DJANGO 6

# Stockage local pour le développement : les produits existants pointent vers
# media/products/, et Django les sert via MEDIA_URL lorsque DEBUG=True.

STORAGES = {

    "default": {
        "BACKEND": (
            "cloudinary_storage.storage.MediaCloudinaryStorage"
            if cloudinary_enabled
            else "django.core.files.storage.FileSystemStorage"
        ),
    },

    "staticfiles": {
        "BACKEND":
        "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },

}


# DEFAULT PRIMARY KEY

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
