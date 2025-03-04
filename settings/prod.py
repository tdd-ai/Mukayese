from .common import *  # noqa: ignore=F405

import os
import raven
import logging

logger = logging.getLogger(__name__)

DEBUG = False

ALLOWED_HOSTS = ["mukayese.tdd.ai"]

# Database
# https://docs.djangoproject.com/en/1.10.2/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.environ.get("POSTGRES_NAME", "evalai"),  # noqa: ignore=F405
        "USER": os.environ.get(  # noqa: ignore=F405
            "POSTGRES_USER", "postgres"
        ),  # noqa: ignore=F405
        "PASSWORD": os.environ.get(  # noqa: ignore=F405
            "POSTGRES_PASSWORD", "postgres"
        ),  # noqa: ignore=F405
        "HOST": os.environ.get(  # noqa: ignore=F405
            "POSTGRES_HOST", "localhost"
        ),  # noqa: ignore=F405
        "PORT": os.environ.get("POSTGRES_PORT", 5432),  # noqa: ignore=F405
    }
}

# DATADOG_APP_NAME = "EvalAI"
# DATADOG_APP_KEY = os.environ.get("DATADOG_APP_KEY")
# DATADOG_API_KEY = os.environ.get("DATADOG_API_KEY")
# MIDDLEWARE += ["middleware.metrics.DatadogMiddleware"]  # noqa

INSTALLED_APPS += ("storages", "raven.contrib.django.raven_compat")  # noqa

AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_SES_REGION_NAME = os.environ.get("AWS_SES_REGION_NAME")
AWS_SES_REGION_ENDPOINT = os.environ.get("AWS_SES_REGION_ENDPOINT")

AWS_SES_ACCESS_KEY_ID =  os.environ.get("AWS_SES_ACCESS_KEY_ID")
AWS_SES_SECRET_ACCESS_KEY = os.environ.get("AWS_SES_SECRET_ACCESS_KEY")

# Amazon S3 Configurations
AWS_S3_CUSTOM_DOMAIN = "%s.s3.amazonaws.com" % AWS_STORAGE_BUCKET_NAME

CORS_ORIGIN_ALLOW_ALL = False

CORS_ORIGIN_WHITELIST = (
    "https://%s.s3.amazonaws.com" % AWS_STORAGE_BUCKET_NAME,
    "https://mukayese.tdd.ai",
)

# static files configuration on S3
STATICFILES_LOCATION = "static"
STATICFILES_STORAGE = "settings.custom_storages.StaticStorage"
STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, STATICFILES_LOCATION)

# Media files configuration on S3
MEDIAFILES_LOCATION = "media"
MEDIA_URL = "http://%s.s3.amazonaws.com/%s/" % (
    AWS_STORAGE_BUCKET_NAME,
    MEDIAFILES_LOCATION,
)
DEFAULT_FILE_STORAGE = "settings.custom_storages.MediaStorage"

# Setup Email Backend related settings
DEFAULT_FROM_EMAIL = "noreply@mukayese.tdd.ai"
# EMAIL_BACKEND = "django_ses.SESBackend"
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_PORT = os.environ.get("EMAIL_PORT")
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS")

# Hide API Docs on production environment
REST_FRAMEWORK_DOCS = {"HIDE_DOCS": True}

# Port number for the python-memcached cache backend.
CACHES["default"]["LOCATION"] = os.environ.get(  # noqa: ignore=F405
    "MEMCACHED_LOCATION"
)  # noqa: ignore=F405

RAVEN_CONFIG = {
    "dsn": os.environ.get("SENTRY_URL"),
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    "release": raven.fetch_git_sha(os.path.dirname(os.pardir)),
}

# https://docs.djangoproject.com/en/1.10/ref/settings/#secure-proxy-ssl-header
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

LOGGING["root"] = {  # noqa
    "level": "INFO",
    "handlers": ["console", "sentry", "logfile"],
}

LOGGING["handlers"]["sentry"] = {  # noqa
    "level": "ERROR",
    "class": "raven.contrib.django.raven_compat.handlers.SentryHandler",
    "tags": {"custom-tag": "x"},
}
