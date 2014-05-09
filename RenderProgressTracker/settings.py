"""
Django settings for RenderProgressTracker project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PARENT_DIR = os.path.dirname(BASE_DIR)

SECRET_KEY = 'tmen^6qgwn@ci0-(^=k#t2zqp0t79!5eotnx_rz0s5+^m3g$@m'

DEBUG = True

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'rest_framework',
    'gunicorn',
    'RenderProgress',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'RenderProgressTracker.urls'

WSGI_APPLICATION = 'RenderProgressTracker.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'render_progress',
        'USER': 'jesse',
        'PASSWORD':'jesse',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = False


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticatedOrReadOnly',),
}

STATIC_ROOT = ''
STATIC_URL = '/static/'
STATICFILES_DIRS = (
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

#import per-app settings to override defaults, before setting up logging
#to override log dir
LOG_DIR = os.path.join(PARENT_DIR, 'django-logs')

try:
    from RenderProgressTracker.local_settings import *
except Exception, e:
    pass


if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
        'no_name': {
            'format': '%(asctime)s [%(levelname)s]: %(message)s'
        }
    },
    'handlers': {
        'default': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'django.log'),
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter':'standard',
        },
        'request_handler': {
                'level':'DEBUG',
                'class':'logging.handlers.RotatingFileHandler',
                'filename': os.path.join(LOG_DIR, 'django_request.log'),
                'maxBytes': 1024*1024*5, # 5 MB
                'backupCount': 5,
                'formatter':'no_name',
        },
        'database': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'django_db.log'),
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter':'no_name',
        },
        'mail_admins': {
            'level':'ERROR',
            'class':'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
        'error_log': {
            'level':'ERROR',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'django_error.log'),
            'maxBytes': 1024*1024*5,
            'backupCount': 5,
            'formatter': 'standard',
        }
    },
    'loggers': {
        '': {
            'handlers': ['default', 'mail_admins', 'error_log'],
            'level': 'DEBUG',
            'propagate': True
        },
        'django.request': {
            'handlers': ['request_handler', 'mail_admins', 'error_log'],
            'level': 'DEBUG',
            'propagate': False
        },
        'django.db.backends': {
            'handlers': ['database', 'mail_admins', 'error_log'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}
