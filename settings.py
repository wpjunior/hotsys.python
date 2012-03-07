#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Trabalho de conclusão de curso
# Alunos
#
# Wilson Pinto Júnior <wilsonpjunior@gmail.com>
# Mateus Fedrigo de Moura <mateusfedrigo@gmail.com>
# Jonathas Peixoto <jonathas.peixoto@gmail.com>
#
# Este programa é um software livre; você pode redistribui-lo e/ou 
# modifica-lo dentro dos termos da Licença Pública Geral GNU como 
# publicada pela Fundação do Software Livre (FSF); na versão 2 da 
# Licença, ou (na sua opnião) qualquer versão.

# Este programa é distribuido na esperança que possa ser  util, 
# mas SEM NENHUMA GARANTIA; sem uma garantia implicita de ADEQUAÇÂO a qualquer
# MERCADO ou APLICAÇÃO EM PARTICULAR. Veja a
# Licença Pública Geral GNU para maiores detalhes.
#
# Você deve ter recebido uma cópia da Licença Pública Geral GNU
# junto com este programa, se não, escreva para a Fundação do Software
# Livre(FSF) Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Wilson Pinto Júnior', 'wilsonpjunior@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'database.db',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

TIME_ZONE = 'America/Sao_Paulo'
LANGUAGE_CODE = 'pt-BR'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
MEDIA_ROOT = ''
MEDIA_URL = ''
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/static/admin/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'commonstatic'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SECRET_KEY = '%4#(l=(itj$h)4*yqc0r3ll6mo3yn&zw2atz#ro3h*%avd=qw_'
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'hotsys.urls'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.contenttypes',
    'hotsys.produto',
    'hotsys.quarto',
    'hotsys.hospede',
    'hotsys.funcionario',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

AUTHENTICATION_BACKENDS = (
    'hotsys.funcionario.backend.LoginBackend',
)

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
