# -*- coding: utf-8 -*-

from curso_de_extensao.settings import *


ALLOWED_HOSTS = ('104.131.39.168',)

DEBUG = False

DB_NAME = 'cursodeextensao'
DB_USER = 'cursodeextensao'
DB_PASSWORD = 'ilikerandompasswords'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
    }
}

STATIC_ROOT = '/opt/static/'
MEDIA_ROOT = '/opt/media/'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = 'igor.canedo@corp.globo.com'
