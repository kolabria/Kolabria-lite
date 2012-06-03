# -*- coding: utf-8 -*-
# Django settings 
import platform
import os
import sys
import pymongo
import bson.objectid
from mongoengine import connect

pymongo.objectid = bson.objectid
sys.modules["pymongo.objectid"] = bson.objectid

ADMINS = (
    (u'admin', 'admin@kolabria.com'),
)

AUTHENTICATION_BACKENDS = (
    'mongoengine.django.auth.MongoEngineBackend',
)
AUTH_PROFILE_MODULE = 'login.UserProfile'

# Database settings
connect('kolabria-new')
#connect('kolabria-324342')


DEBUG = True
TEMPLATE_DEBUG = DEBUG

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
)

PATH = os.path.dirname(__file__)

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'testkolabria@gmail.com'
EMAIL_HOST_PASSWORD = 'test_kolabria'
EMAIL_PORT = 587

FILE_UPLOAD_PERMISSIONS = 0644
FROM_EMAIL = EMAIL_HOST_USER

INTERNAL_IPS = ('127.0.0.1',)

LOGIN_REDIRECT_URL = '/devices/'
LOGIN_URL = '/login/'

MEDIA_ROOT = PATH + '/media/'
MEDIA_URL = '/media/' 

SITE_ID = 1
STATIC_ROOT = PATH + 'static/'
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    PATH + '/static',
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

LANGUAGE_CODE = 'en-us'
MANAGERS = ADMINS

ROOT_URLCONF = 'urls'
SECRET_KEY = '8!xvqfrfretert45564y6565655566ythhhhhh&k0c@ru)v'
SESSION_ENGINE = 'mongoengine.django.sessions'

TEMPLATE_DIRS = (
    PATH + '/templates',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TIME_ZONE = 'America/Montreal'

USE_I18N = False
USE_L10N = False

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
#    'main',
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

TEMPLAGE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.media',
    'django.contrib.messages.middleware.MessageMiddleware',
    'context_processors.auth',
    'context_processors.site_info',
)
