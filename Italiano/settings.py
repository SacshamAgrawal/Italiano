# settings.py
from dotenv import load_dotenv
load_dotenv()

# from pprint import pprint
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR,'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')
MEDIA_DIR = os.path.join(BASE_DIR, 'media')
MEDIA_ROOT = MEDIA_DIR

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    
    'channels',
    'login',
    'pizza',
    'rest_framework',
    
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',

    'phonenumber_field',
    'django_cleanup.apps.CleanupConfig',
    'mathfilters',
    'django_extensions',
    'webpack_loader',
    'debug_toolbar',
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES':(
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES':(
        'rest_framework.permissions.DjangoModelPermissions',
    ),
    'DEFAULT_FILTER_CLASSES':(
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_PAGINATION_CLASS':'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE':100,
}

LOGGING = {
    'version':1,
    'disable_existing_loggers':False,
    'handlers':{
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
        },
    },
    'loggers':{
        'login':{
            'level': 'INFO',
            'handlers':['console',],
            'propagate':True,
        },
        'pizza':{
            'level': 'DEBUG',
            'handlers':['console',],
            'propagate':True,
        },
    }
}

INTERNAL_IPS = [
    '127.0.0.1',
]

EMAIL_BACKEND='django.core.mail.backends.console.EmailBackend'
PHONENUMBER_DEFAULT_REGION = 'IN'
SITE_ID = '1'

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'email' 
ACCOUNT_EMAIL_REQUIRED = True
#ACCOUNT_EMAIL_VERIFICATION = 'mandatory' 
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_LOGOUT_ON_GET = True
AUTH_USER_MODEL = 'login.User'
ACCOUNT_FORMS = {
        'signup':'login.forms.CustomSignupForm',
    }

# Login redirection URLs
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = 'homepage'
LOGOUT_REDIRECT_URL = 'homepage'

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'pizza.middlewares.cart_middleware',
]

ROOT_URLCONF = 'Italiano.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR,],
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

CACHES = {
    'default' : {
        'BACKEND' : 'django.core.cache.backends.dummy.DummyCache',
        'LOCATION' : 'localhost:8000',
    }
}

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': os.environ.get('GOOGLE_CLIENT_ID'),
            'secret': os.environ.get('GOOGLE_SECRET'),
            'key': ''
        }
    }
}

WSGI_APPLICATION = 'Italiano.wsgi.application'
ASGI_APPLICATION = 'Italiano.routing.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': "fooddelivery",
        'USER':os.environ.get('PSQL_DB_USER'),
        'PASSWORD' : os.environ.get('PSQL_DB_PASSWORD'),
        'HOST':'localhost',
        'PORT':5432,
    }
}

CHANNEL_LAYERS = {
    'default':{
        'BACKEND':'channels_redis.core.RedisChannelLayer',
        'CONFIG':{
            'hosts':[('127.0.0.1',6379),],
        }
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
)

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR,'root')
STATICFILES_DIRS = [STATIC_DIR, ]
MEDIA_URL = '/media/'  