# -*- coding: utf-8 -*-

"""
Django settings for curso_de_extensao project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS, AUTHENTICATION_BACKENDS
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

ADMIN = (
    ('Igor Canedo', 'igor.canedo@corp.globo.com',),
)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '3is#d^%m#)a4e^y$yz8vi$n+p9euj#o9xvs9te9-12_fw2ahk@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

THIRD_PARTY_APPS = (
    'localflavor',
    'bootstrap3',
)


PROJECT_APPS = (
    'core',
    'pessoa',
    'disciplina',
    'portal',
    'downloads',
)

INSTALLED_APPS += THIRD_PARTY_APPS + PROJECT_APPS

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'curso_de_extensao.urls'

WSGI_APPLICATION = 'curso_de_extensao.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DB_USER = 'cursodeextensao'
DB_PASSWORD = 'ilikerandompasswords'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'cursodeextensao',
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.request',
)

BOOTSTRAP3 = {
    'include_jquery': True,
    'jquery_url': '/static/js/jquery-2.1.1.min.js',
}

AUTH_USER_MODEL = 'pessoa.Pessoa'

AUTHENTICATION_BACKENDS += ('pessoa.backend.CustomBackend',)

BUSINESS = {
    'media_aprovacao': 5,
}

IFRAME_URL = 'http://www.del.ufrj.br/~fmello/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'cursodeextensao.del@gmail.com '
EMAIL_HOST_PASSWORD = 'q1w2E#R$'

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
