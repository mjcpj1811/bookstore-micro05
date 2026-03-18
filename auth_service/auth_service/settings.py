import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'auth-service-secret-key-change-in-production'
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'rest_framework',
    'corsheaders',
    'auth_app',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'auth_service.urls'
WSGI_APPLICATION = 'auth_service.wsgi.application'
CORS_ALLOW_ALL_ORIGINS = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'auth_db',
        'USER': os.environ.get('DB_USER', 'root'),
        'PASSWORD': os.environ.get('DB_PASSWORD', '123456'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '3306'),
        'OPTIONS': {'charset': 'utf8mb4'},
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': ['rest_framework.renderers.JSONRenderer'],
}

SERVICE_URLS = {
    'CUSTOMER_SERVICE': os.environ.get('CUSTOMER_SERVICE_URL', 'http://localhost:8003'),
    'STAFF_SERVICE': os.environ.get('STAFF_SERVICE_URL', 'http://localhost:8001'),
    'MANAGER_SERVICE': os.environ.get('MANAGER_SERVICE_URL', 'http://localhost:8002'),
}

# Shared JWT secret between auth-service and API gateway.
# Để tránh lệch cấu hình giữa Docker và chạy local, ta
# dùng cố định một chuỗi secret cho cả hai service.
JWT_SECRET = 'bookstore-jwt-secret-dev'
JWT_ALGORITHM = 'HS256'
JWT_EXP_SECONDS = int(os.environ.get('JWT_EXP_SECONDS', '86400'))  # 1 day
