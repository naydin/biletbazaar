# Django settings for biletbazaar project.
from local_settings import *


DEBUG = LOCAL_DEBUG
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
    LOCAL_ADMIN
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': LOCAL_DATABASE_NAME,                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': LOCAL_DATABASE_USER,
        'PASSWORD': LOCAL_DATABASE_PASSWORD,
        'HOST': LOCAL_DATABASE_HOST,                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': LOCAL_DATABASE_PORT,                      # Set to empty string for default.
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['www.biletbosta.com','biletbosta.com']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.w
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = LOCAL_MEDIA_ROOT

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = LOCAL_MEDIA_URL

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"

import os
STATIC_ROOT = LOCAL_STATIC_ROOT
STATIC_TEMP_ROOT = os.path.join(os.path.abspath(os.path.dirname(__file__)), "statictemp")

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = LOCAL_STATIC_URL

# Additional locations of static files
STATICFILES_DIRS = (
    STATIC_TEMP_ROOT,
    # "/Users/naydin/downloads/folder",
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '@ml@&+5ci(-=hzsw+dj%h_956$(36sb!d_(36*y%s-7j*1l$=@'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
ROOT_URLCONF = 'biletbazaar.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'biletbazaar.wsgi.application'

import os.path
TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'Templates').replace('\\','/'),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)


TEMPLATE_CONTEXT_PROCESSORS = ('biletbazaar.context_processors.autocomplete_tags','django.contrib.auth.context_processors.auth')

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    'data',
    'sell',
    'buy',
    'events',
)



AUTOLOAD_TEMPLATETAGS = (
    'events.templatetags.extra_tags',
)


SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
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

from auth_backends import *

AUTHENTICATION_BACKENDS = (
    'biletbazaar.auth_backends.PasswordlessAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
)

EMAIL_HOST = LOCAL_EMAIL_HOST
EMAIL_HOST_USER = LOCAL_EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = LOCAL_EMAIL_HOST_PASSWORD
DEFAULT_FROM_EMAIL = LOCAL_DEFAULT_FROM_EMAIL
SERVER_EMAIL = LOCAL_SERVER_EMAIL

AUTH_USER_MODEL = 'data.User'
