# Django settings for basque_research project.
import os, sys, socket
BASEDIR = os.path.dirname(__file__)
sys.path.insert(0, BASEDIR)


## ADI, SETTINGS-AK EZBERDIN JOANGO DIRA ####
SMTP_SERVER="localhost"
DEFAULT_FROM_EMAIL='basqueresearch@elhuyar.com'
DEFAULT_TO_EMAIL="i.manterola@elhuyar.com"
BASE_URL = "http://basqueresearch.elh"


DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Iker', 'i.manterola@elhuyar.com'),
    ('Maddalen', 'm.lopezdelacalle@elhuyar.com'),
)

HIZKUNTZAK={
1:['eu','Euskara'],
2:['es','Gaztelera'],
3:['en','Ingelesa'],
#4:['fr','Frantsesa']
}




MANAGERS = ADMINS

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = ()
####################################

'''CACHES = {
    'default': {
    'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
    'LOCATION': 'basque_research_cache_table',
}
}'''

#BASE_URL="http://10.0.0.164:8008"
DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'kulturbideak_db',                      # Or path to database file if using sqlite3.
            # The following settings are not used with sqlite3:
            'USER': 'root',
            'PASSWORD': 'llm_F054',
            'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
            'PORT': '',                      # Set to empty string for default.
        },      
    }


    ####################################

## LOCALEAK non dauden jakiteko
LOCALE_PATHS = (
    os.path.join(BASEDIR, 'locale'),
)

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
# Itziar. Gora pasa dut aldagaia
# ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Madrid'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'eu'

LANGUAGES = (
    ('eu', 'eu'),
    ('en', 'en'), 
    ('es', 'es'),
    #('fr', 'fr'),
       
)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = os.path.join(BASEDIR, 'kulturbideak_app/media/uploads/')


# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/uploads/'


LOGIN_URL="/login"

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(BASEDIR, 'kulturbideak_app/static')

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    #'static/',
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
SECRET_KEY = 'sfvj$4ii80%6*+&h$tg97lg-=v^jk#)36vb&-6nze7*4%9ek2^'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
  'django.contrib.auth.context_processors.auth',
  'django.core.context_processors.i18n',
  'django.core.context_processors.request',
  'django.core.context_processors.media',
  'django.core.context_processors.static',

    ) # Optional

#TEMPLATE_CONTEXT_PROCESSORS = (
#    'django.core.context_processors.i18n',
#)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'KULTURBIDEAK.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'KULTURBIDEAK.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
	os.path.join(BASEDIR, 'kulturbideak_templates'),
    os.path.join(BASEDIR, 'kulturbideak_app'),
)

RECAPTCHA_PUBLIC_KEY = '6LcxY-USAAAAAP_Gxwnsha9tdpEaFCbSPPpMq7dZ'
RECAPTCHA_PRIVATE_KEY = '6LcxY-USAAAAAPEzzoc1AOiAoSMgiGzbA0RyAsUB'


INSTALLED_APPS += (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
     'django.contrib.admin',
    # Added.
    'haystack',
    'bootstrap3',
    #'rosetta',
    'KULTURBIDEAK.kulturbideak_app',
   

    #'south',
    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

# Maddalen- Haystack
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://127.0.0.1:8983/solr'
        # ...or for multicore...
        # 'URL': 'http://127.0.0.1:8983/solr/mysite',
    },
}
# Maddalen- Haystack
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
