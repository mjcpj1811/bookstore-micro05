import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'api-gateway-secret-key-change-in-production'
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'rest_framework',
    'corsheaders',
    'gateway',
]

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'api_gateway.urls'
WSGI_APPLICATION = 'api_gateway.wsgi.application'
CORS_ALLOW_ALL_ORIGINS = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
            ],
        },
    },
]

STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_URL = '/static/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Microservice URLs
SERVICE_URLS = {
    'STAFF_SERVICE': os.environ.get('STAFF_SERVICE_URL', 'http://localhost:8001'),
    'MANAGER_SERVICE': os.environ.get('MANAGER_SERVICE_URL', 'http://localhost:8002'),
    'CUSTOMER_SERVICE': os.environ.get('CUSTOMER_SERVICE_URL', 'http://localhost:8003'),
    'CATALOG_SERVICE': os.environ.get('CATALOG_SERVICE_URL', 'http://localhost:8004'),
    'BOOK_SERVICE': os.environ.get('BOOK_SERVICE_URL', 'http://localhost:8005'),
    'CART_SERVICE': os.environ.get('CART_SERVICE_URL', 'http://localhost:8006'),
    'ORDER_SERVICE': os.environ.get('ORDER_SERVICE_URL', 'http://localhost:8007'),
    'SHIP_SERVICE': os.environ.get('SHIP_SERVICE_URL', 'http://localhost:8008'),
    'PAY_SERVICE': os.environ.get('PAY_SERVICE_URL', 'http://localhost:8009'),
    'COMMENT_RATE_SERVICE': os.environ.get('COMMENT_RATE_SERVICE_URL', 'http://localhost:8010'),
    'RECOMMENDER_AI_SERVICE': os.environ.get('RECOMMENDER_AI_SERVICE_URL', 'http://localhost:8011'),
}
