"""
Django settings for analytics project.

Generated by 'django-admin startproject' using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from pathlib import Path
from typing import Any, Dict, List

BASE_DIR: str = Path(__file__).resolve().parent.parent

SECRET_KEY: str = "django-insecure-26bol5n4brr!k79%qu*)3v*s*ld^3aw^nogtu4mzdxdoo8o5^g"

DEBUG: bool = True

ALLOWED_HOSTS: List[str] = [
    "127.0.0.1",
]

INSTALLED_APPS: List[str] = [
    # Django standard applications.
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Django third-party libraries.
    "rest_framework",
    "wrapwith",
    "mathfilters",

    # Application blueprints.
    "clients",
    "audiences",
    "countries",
    "states",
    "cities",
    "campaigns",
    "pages",
    "metadata",
    "metrics",
    "events",
    "subscriptions",
    "products",
    "reports",
]

MIDDLEWARE: List[str] = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF: str = "analytics.urls"

TEMPLATES: List[Dict[str, Any]] = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            "templates",
            os.path.join(BASE_DIR, "analytics", "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION: str = "analytics.wsgi.application"

DATABASES: Dict[str, Dict[str, str]] = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS: List[Dict[str, str]] = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE: str = "en-us"

TIME_ZONE: str = "UTC"

USE_I18N: bool = True

USE_L10N: bool = True

USE_TZ: bool = True

STATIC_URL: str = "/static/"
STATIC_ROOT: str = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS: List[str] = [
    os.path.join(BASE_DIR, "analytics", "static"),
]

DEFAULT_AUTO_FIELD: str = "django.db.models.BigAutoField"

REST_FRAMEWORK: Dict[str, Any] = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ]
}

LOGGING: Dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[+] {asctime} [{levelname}] {module}.py pid={process:d} tid={thread:d}: {message}",
            "style": "{",
        },
        "simple": {
            "format": "[+] [{levelname}] {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple" if DEBUG else "verbose",
        },
        "file": {
            "level": "DEBUG" if DEBUG else "WARNING",
            "class": "logging.FileHandler",
            "filename": os.path.join(os.sep, "tmp", "analytics.log"),
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "DEBUG" if DEBUG else "WARNING",
    },
}

LOGIN_REDIRECT_URL: str = 'dashboard'
LOGIN_URL: str = 'rest_framework:login'
