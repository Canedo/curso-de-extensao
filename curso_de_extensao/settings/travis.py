# -*- coding: utf-8 -*-
from curso_de_extensao.settings import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '',
        'USER': 'travis',
    }
}
