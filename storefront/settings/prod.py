import os
import dj_database_url
from .common import *

DEBUG = False

SECRET_KEY = os.environ['SECRET_KEY'] 

ALLOWED_HOSTS = ['jiebuy-f97dfef19743.herokuapp.com']

DATABASES = {
    'default': dj_database_url.config()
}

REDIS_URL = os.environ['REDISCLOUD_URL']

CELERY_BROKER_URL = REDIS_URL

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
} 

EMAIL_HOST =  'localhost'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 2525
DEFAULT_FROM_EMAIL = 'from@moshy.com'
