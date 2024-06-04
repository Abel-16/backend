"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
import datetime
from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ouszk%3j%bzc(m1!r6)17mx2e_i7!eprus35ts(-*wl2=2h@at'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*','https://web-front-end-coral.vercel.app','http://localhost:3000/']

# AUTH_USER_MODEL = 'authentication.User'



CORS_ALLOWED_ORIGINS = [
    "https://web-front-end-coral.vercel.app",
    "http://localhost:8080",
    "http://127.0.0.1:9000",
    "https://web-front-5u00dzsf6-ab3lts-projects.vercel.app",
]
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://web-front-end-coral.vercel.app",
]

# Application definition

INSTALLED_APPS = [
    
      'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
      'django_chapa',
    'corsheaders',
    # 'authentication',
    'drf_yasg',
    'rest_framework',
    'api',
    'website',
    # 'store',
    'payment',
    'userauths',
    'store',
    'farmer',

]

CHAPA_SECRET_KEY = "CHASECK_TEST-VJfumVrsShqDRBsczJsnS2tRF0CKaR04"

CHAPA_API_URL = 'https://api.chapa.co/v1/transaction/initialize'

CHAPA_API_VERSION = 'v1'


MIDDLEWARE = [
    
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.common.CommonMiddleware',
    
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'backend.wsgi.application'
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR, 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

AUTH_USER_MODEL = 'userauths.User'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

REST_FRAMEWORK={
    'NON_FIELD_ERRORS_KEY' : 'error',
     'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
          'rest_framework.authentication.TokenAuthentication',
    )
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": datetime.timedelta(minutes=10),
    "REFRESH_TOKEN_LIFETIME": datetime.timedelta(days=1),
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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#email configuration
# EMAIL_USE_TLS = False
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = '127.0.0.1'
# EMAIL_PORT = 1025
# EMAIL_HOST_USER = ''
# EMAIL_HOST_PASSWORD = ''
# Email backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# SMTP server settings for Gmail
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'abelt.alx@gmail.com'
EMAIL_HOST_PASSWORD = 'ecvlauoljxtqaqaf'
EMAIL_USE_TLS = True

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS' : {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'id': 'header'
        }
    }
}


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME' :timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME':timedelta(days=50),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION':True,
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS256',
    'VERIFYING_KEY': None,
    'ISSUER': None,
    'JWK_URL' : None,
    'LEEWAY' : 0,
    'AUTH_HEADER_TYPES' : ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_aUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',
    
    
    
    
}

JAZZMIN_SETTINGS={
    'site_title' : "Agristore",
    'site_header' :'Agriculture Products',
    'site_brand' :'Welcome to Agriculture ',
    'welcome_sign' :'Welcome to Agriculture ',
    'copyright' :'AAiT Agriculture ',
    'show_sidebar': True,
    # 'show_ui_builder': True
    
}

JAZZMIN_UI_TWEAKS = {
 
    "theme": "minty",
    "dark_mode_theme": "solar ",
}


CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True