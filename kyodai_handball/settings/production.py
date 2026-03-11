from .base import *

SECRET_KEY = "django-insecure-msb=r@t$(c#*6qtpb2t03vuh1a=!sz1fi5w7q0pfnu73(v67r6"

DEBUG = False
ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS = ["https://kyodai-handball.com"]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
WAGTAIL_ENABLE_UPDATE_CHECK = False

STORAGES["staticfiles"]["BACKEND"] = "whitenoise.storage.CompressedManifestStaticFilesStorage"

try:
    from .local import *
except ImportError:
    pass