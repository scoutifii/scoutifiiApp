from pathlib import Path
from django.core.management.commands.runserver import Command as rs
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = True 
DEBUG = os.environ.get('DJANGO_DEBUG', 0) != 'False'

ALLOWED_HOSTS = ['scoutifii.com', '127.0.0.1', 'localhost']

ALLOWED_HOSTS_ENV = os.environ.get('ALLOWED_HOSTS')
if ALLOWED_HOSTS_ENV:
    ALLOWED_HOSTS.extend(ALLOWED_HOSTS_ENV.split(','))


rs.default_port='5000'

# Application definition

INSTALLED_APPS = [
    # 'daphne',
    'jazzmin',    
    'django.contrib.humanize',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'scoutifiiapp.apps.Scoutify2Config',
    'django_countries',
    'dbbackup',
    'channels',
    'crispy_forms',
    'rest_framework',
    'corsheaders',
     ## 3rd party
    'rest_framework_swagger',

    # testing etc:
    'django_jenkins',
    'django_extensions',
    # 'django.contrib.staticfiles', # Required for GraphiQL
    'graphene_django',
]

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "django.middleware.cache.UpdateCacheMiddleware",
    'django.middleware.common.CommonMiddleware',
    "django.middleware.cache.FetchFromCacheMiddleware",
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_otp.middleware.OTPMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'scoutifiiapp.middleware.CustomActivityLog',
]

ROOT_URLCONF = 'scoutifiiapp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'scoutifiiapp.views.count_notifications',
            ],
        },
    },
]

WSGI_APPLICATION = 'scoutifiiapp.wsgi.application'
ASGI_APPLICATION = 'scoutifiiapp.asgi.application'

# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get("MYSQL_DB"),
        'USER': os.environ.get("MYSQL_USER"),
        'PASSWORD': os.environ.get("MYSQL_PASSWORD"),
        'PORT': int(os.environ.get("MYSQL_PORT")),
        'HOST': os.environ.get("MYSQL_HOST"),
        'DB_IGNORE_SSL': os.environ.get("DB_IGNORE_SSL") == "true",
        'OPTIONS': {
            # 'init_command': 'SET default_storage_engine=INNODB',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES', innodb_strict_mode=1",
            'charset': 'utf8mb4',
            "autocommit": True,
        }
    }
}

db_ignore_ssl = 'DB_IGNORE_SSL'
if not db_ignore_ssl:
    DATABASES["default"]["OPTIONS"] = {
        "sslmode": "require"
    }

# # # set this to False if you want to turn off pyodbc's connection pooling
# # DATABASE_CONNECTION_POOLING = False

DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_STORAGE_OPTIONS = {'location': BASE_DIR/'backup/'}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
        # "BACKEND": "channels_redis.core.RedisChannelLayer",
        # "CONFIG": {
        #     "hosts": [("127.0.0.1", 6379)],
        # },
    },
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.locmem.LocMemCache",
        # "BACKEND": "django.core.cache.backends.redis.RedisCache",
        # "LOCATION": "redis://127.0.0.1:6379",
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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


# Internationalization

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Nairobi'
USE_I18N = True
USE_TZ = False


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATICFILES_DIRS = os.path.join(BASE_DIR, 'staticfiles'),
STATIC_ROOT = os.path.join(BASE_DIR, 'scoutifiiapp', 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

SESSION_SAVE_EVERY_REQUEST = True

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

SESSION_COOKIE_AGE = 10800

SESSION_ENGINE = "django.contrib.sessions.backends.cache"

# HTTPS Settings
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True

# HSTS Settings
SECURE_HSTS_SECONDS = 31536000 # 1 Year
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# X-XSS-Protection
SECURE_BROWSER_XSS_FILTER = True


# Cache Control
CACHE_MIDDLEWARE_ALIAS = "default"
CACHE_MIDDLEWARE_SECONDS = 600
CACHE_MIDDLEWARE_KEY_PREFIX = ''

# Allow upload of big file of 20MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024 * 20  
FILE_UPLOAD_MAX_MEMORY_SIZE = DATA_UPLOAD_MAX_MEMORY_SIZE

#SMTP Configuration

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'masiga_2005@gmail.com'
EMAIL_HOST_PASSWORD = ''

#JAZZMIN Configuration

JAZZMIN_SETTINGS = {
    "site_header": "Admin Panel",
    "site_title": "Scoutifii Admin",
    "site_logo": "assets/images/scoutifii3.jpg",
    "login_logo": "assets/images/scoutifii3.jpg",
    "welcome_sign": "Welcome to Scoutifii",
    "copyright": "Scoutifii",
    "show_sidebar": True,
    "site_width": 20,
    "site_height": 20,

    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
    },
}

CRISPY_TEMPLATE_PACK = 'uni_form'
CORS_ALLOW_ALL_ORIGINS = True

LOGIN_URL = 'two_factor:login'

# CUSTOM AUTH
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    # 'tokenauth.authbackends.TokenAuthBackend'
)

## REST
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        ## we need this for the browsable API to work
        'rest_framework.authentication.SessionAuthentication',
        # 'tokenauth.authbackends.RESTTokenAuthBackend',
    )
}

# Services:

## Service base urls without a trailing slash:
# USER_SERVICE_BASE_URL = 'http://staging.userservice.tangentme.com'

JENKINS_TASKS = (
    'django_jenkins.tasks.run_pylint',
    'django_jenkins.tasks.with_coverage',
)

ACCOUNT_SID='YOUR ACCOUNT SID'
AUTH_TOKEN='YOUR AUTH TOKEN'
COUNTRY_CODE='+256'
TWILIO_WHATSAPP_NUMBER='whatsapp:+14155238886'
TWILIO_PHONE_NUMBER='number you get from Twilio'

GRAPHENE = {
  'SCHEMA': 'graph.schema.schema'
}
