"""
Django settings for invt project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-_vbv5@-seref1e856*a%0#@sfyke1%3&eyq*c)%-4v_*yonbj'


ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'invt',
    'rest_framework',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'invt.middleware.MobileRedirectMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'invt.urls'

WSGI_APPLICATION = 'invt.wsgi.application'



if 'SERVER_SOFTWARE' in os.environ:
    from sae.const import (
        MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASS, MYSQL_DB
    )

else:
    # Make `python manage.py syncdb` works happy!
    MYSQL_HOST = 'localhost'
    MYSQL_PORT = '3306'
    MYSQL_USER = 'root'
    MYSQL_PASS = 'luoluo'
    MYSQL_DB   = 'invt'

DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.mysql',
#        'STORAGE_ENGINE': 'MYISAM',
#        'STORAGE_ENGINE': 'INNODB',
#        'OPTIONS'  : { 'init_command' : 'SET storage_engine=MYISAM' },
        'NAME':     MYSQL_DB,
        'USER':     MYSQL_USER,
        'PASSWORD': MYSQL_PASS,
        'HOST':     MYSQL_HOST,
        'PORT':     MYSQL_PORT,
        'TEST_CHARSET': 'UTF8',
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Shanghai'
LANGUAGE_CODE = 'zh-cn'

USE_I18N = True

USE_L10N = True

USE_TZ = True


DEBUG = True
TEMPLATE_DEBUG = True

STATIC_URL = '/m/'
# static file setting is not necessary in SAE
if not 'SERVER_SOFTWARE' in os.environ:

    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, "static"),
        '/Users/mac/Projects/Invitation/Front/'
    )

    #Upload location
    MEDIA_ROOT = '/Users/mac/ME/Media/'
    MEDIA_URL = '/u/'

    #Database migration
    INSTALLED_APPS += ('south',)

    from django.core.files.storage import FileSystemStorage
    STORAGE = FileSystemStorage(location=MEDIA_ROOT)

else:
    from invt.saestorage import SaeStorage
    STORAGE = SaeStorage('imgs')
    DEBUG = False
    TEMPLATE_DEBUG = False

#
TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates'),
)

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('invt.permission.IsOwnerOrReadOnly',
                                   'invt.permission.IsAuthenticatedOrReadOnly',),
}

#CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = (
    'localhost:8080',
)
