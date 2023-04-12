import os
from pathlib import Path

import rollbar
from configurations import Configuration
from environs import Env

env = Env()
env.read_env()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


class Dev(Configuration):
    SECRET_KEY = env("SECRET_KEY")
    DEBUG = True

    ALLOWED_HOSTS = ["*"]

    INSTALLED_APPS = [
        "foodcartapp.apps.FoodcartappConfig",
        "restaurateur.apps.RestaurateurConfig",
        "geocache.apps.GeocacheConfig",
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "debug_toolbar",
        "phonenumber_field",
        "rest_framework",
    ]

    MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
        "debug_toolbar.middleware.DebugToolbarMiddleware",
        "rollbar.contrib.django.middleware.RollbarNotifierMiddlewareExcluding404",
    ]

    ROOT_URLCONF = "star_burger.urls"

    DEBUG_TOOLBAR_PANELS = [
        "debug_toolbar.panels.versions.VersionsPanel",
        "debug_toolbar.panels.timer.TimerPanel",
        "debug_toolbar.panels.settings.SettingsPanel",
        "debug_toolbar.panels.headers.HeadersPanel",
        "debug_toolbar.panels.request.RequestPanel",
        "debug_toolbar.panels.sql.SQLPanel",
        "debug_toolbar.panels.staticfiles.StaticFilesPanel",
        "debug_toolbar.panels.templates.TemplatesPanel",
        "debug_toolbar.panels.cache.CachePanel",
        "debug_toolbar.panels.signals.SignalsPanel",
        "debug_toolbar.panels.logging.LoggingPanel",
        "debug_toolbar.panels.redirects.RedirectsPanel",
    ]

    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [
                BASE_DIR / "templates",
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

    WSGI_APPLICATION = "star_burger.wsgi.application"

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
    DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

    AUTH_PASSWORD_VALIDATORS = [
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

    LANGUAGE_CODE = "ru-RU"

    TIME_ZONE = "Europe/Moscow"

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    STATIC_URL = "/static/"
    STATIC_ROOT = BASE_DIR / "staticfiles"
    MEDIA_ROOT = BASE_DIR / "media"
    MEDIA_URL = "/media/"
    INTERNAL_IPS = ["127.0.0.1"]

    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "assets"),
        os.path.join(BASE_DIR, "bundles"),
    ]


class Prod(Dev):
    DEBUG = False
    ROLLBAR = {
        "access_token": env.str("rollbar_token", None),
        "environment": env.str("rollbar_env", "Test"),
        "root": BASE_DIR,
    }
    rollbar.init(**ROLLBAR)


class ProdPostgres(Prod):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": env.str("PG_DB_NAME", None),
            "USER": env.str("PG_USER", None),
            "PASSWORD": env.str("PG_PASS", None),
        }
    }
