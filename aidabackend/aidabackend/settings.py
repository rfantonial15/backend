import os
from pathlib import Path
from datetime import timedelta

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-t)_xfp@&7o1!+vhfzv8mv+fzjaefi*8_uj_mt9$@b)k6%h9%i0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False  # Set to False for deployment

ALLOWED_HOSTS = ['*']  # Replace '*' with specific domains for production

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt',
    'reports',
    'datas',
    'alert',
    'storages',
    'channels',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Added for static file handling
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://your-production-domain",
]

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = ['Authorization', 'Content-Type']
CORS_ALLOW_METHODS = ['DELETE', 'GET', 'OPTIONS', 'PATCH', 'POST', 'PUT']

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'aida.response@gmail.com'
EMAIL_HOST_PASSWORD = 'kcka vkjw fkxh xezk'  # Replace with actual email password
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

FRONTEND_URL = 'http://localhost:5173/'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

ROOT_URLCONF = 'aidabackend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

# Database Configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'aidabackend_db',
        'USER': 'aida_user',
        'PASSWORD': 'securepassword123',  # Replace with actual database password
        'HOST': 'localhost',  # Replace with your database host
        'PORT': '5432',  # Default PostgreSQL port
    }
}

AUTH_USER_MODEL = "datas.User"

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Manila'
USE_I18N = True
USE_TZ = True

# AWS S3 Configuration
AWS_ACCESS_KEY_ID = 'AKIA2ZIONDAYGELBG7TS'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'aida-report001'
AWS_S3_REGION_NAME = 'ap-southeast-2'
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
AWS_QUERYSTRING_AUTH = False

MEDIA_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com/media/'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = (
    'storages.backends.s3boto3.S3StaticStorage' if not DEBUG else 'whitenoise.storage.CompressedManifestStaticFilesStorage'
)

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [os.environ.get('REDIS_TEMPORARY_URL', 'redis://:pd014eb2cb388addb598176011956aa1c693af994cb051cb1091703afeae38013@ec2-52-200-199-24.compute-1.amazonaws.com:27779')],
        },
    },
}

ASGI_APPLICATION = 'aidabackend.asgi.application'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
