import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-a!rksd6rrnp2&mw%$%=-b$ffb6r&9rglmvj*%4n(he)p2q^^rt')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '').split(',')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_celery_results',
    'corsheaders',
    'apps.webhook_handler',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # Deve vir antes do CommonMiddleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'realmate_challenge.urls'

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

WSGI_APPLICATION = 'realmate_challenge.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_ENGINE', 'django.db.backends.postgresql'),
        'NAME': os.environ.get('DB_NAME', 'realmate'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'postgres'),
        'HOST': os.environ.get('DB_HOST', 'postgres'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Django REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
}

# Celery Configuration
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'django-cache'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True  # Added to address deprecation warning

# Configurações de throttle
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_RATES': {
        'webhook': '60/minute',  # Ajuste conforme necessário
    }
}

# Configurações CORS
CORS_ALLOW_ALL_ORIGINS = DEBUG  # Permite todas as origens em desenvolvimento
if not DEBUG:
    CORS_ALLOWED_ORIGINS = [
        # Adicione aqui as origens permitidas em produção
        # Ex: "https://exemplo.com"
    ]
    CORS_ALLOW_CREDENTIALS = True

if DEBUG:
    # Configuração de segurança para desenvolvimento
    WEBHOOK_API_KEY = os.environ.get('WEBHOOK_API_KEY', 'debug')
    ALLOWED_HOSTS = ['localhost', '127.0.0.1'] + ALLOWED_HOSTS
else:
    # Configuração de segurança para produção
    # Força o redirecionamento de todas as requisições HTTP para HTTPS
    SECURE_SSL_REDIRECT = True
    
    # Garante que os cookies de sessão só sejam enviados através de HTTPS
    SESSION_COOKIE_SECURE = True
    
    # Garante que os cookies CSRF só sejam enviados através de HTTPS
    CSRF_COOKIE_SECURE = True
    
    # Ativa o filtro XSS (Cross-Site Scripting) do navegador
    SECURE_BROWSER_XSS_FILTER = True
    
    # Impede que o navegador tente adivinhar o tipo de conteúdo (MIME sniffing)
    SECURE_CONTENT_TYPE_NOSNIFF = True
    
    # Define o tempo que o navegador deve lembrar que o site só deve ser acessado via HTTPS (1 ano)
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    
    # Aplica a política HSTS também para os subdomínios
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    
    # Permite que o site seja pré-carregado na lista HSTS dos navegadores
    SECURE_HSTS_PRELOAD = True
    
    # Impede que o site seja carregado em um iframe (proteção contra clickjacking)
    X_FRAME_OPTIONS = 'DENY'
    
    # Chave secreta para validação de webhooks
    WEBHOOK_SECRET = os.environ.get('WEBHOOK_SECRET')

    # Configuração de logs
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '[{levelname}] {asctime} {module} - {message}',
                'style': '{',
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'verbose',
            },
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': True,
            },
            'webhook_handler': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': True,
            },
            'celery': {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': True,
            },
        },
    }
