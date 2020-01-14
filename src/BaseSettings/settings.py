﻿"""
Django settings for BaseSettings project.

Generated by 'django-admin startproject' using Django 1.10.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
import os.path
from django.conf.urls.static import static
from django.utils.translation import ugettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "u3c*b4jd&+vvvcv@p5hr#fr$1kn1=9x)1=yiysz0m^32iuqrl&"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Application definition
# Add application here
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django_template_maths",
    "livesync",
    "django.contrib.staticfiles",
    "Users",
    "SmsBaseApp",
    "SmsBackEnd",
    "online_users",
    "Equipment",
    "Team",
]
FILE_UPLOAD_HANDLERS = (
    "django_excel.ExcelMemoryFileUploadHandler",
    "django_excel.TemporaryExcelFileUploadHandler",
)

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # 'livesync.core.middleware.DjangoLiveSyncMiddleware',
    "online_users.middleware.OnlineNowMiddleware",
]

DJANGO_LIVESYNC = {"PORT": 8000}  # this is optional and is default set to 9001.

ROLEPERMISSIONS_MODULE = "BaseSettings.roles"

ROOT_URLCONF = "BaseSettings.urls"
SESSION_SAVE_EVERY_REQUEST = True

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            "SmsBaseApp/templates",
            "Users/templates",
            "Team/templates",
            "Equipment/templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.media",
                # 'django.core.context_processors.i18n',
            ]
        },
    }
]

WSGI_APPLICATION = "BaseSettings.wsgi.application"

# Database config
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    "default": {
        "NAME": "db_test",  # ชื่อฐานข้อมูล
        "ENGINE": "django.db.backends.mysql",  # <- window
        # 'ENGINE': 'mysql.connector.django', #  <- linux
        "OPTIONS": {"sql_mode": "traditional", "use_unicode": True},
        "USER": "root3",  # ชื่อผู้ใช้
        "PASSWORD": "",  # รหัสผ่าน
        "HOST": "127.0.0.1",  # โฮมฐานข้อมูล
        "PORT": "41063",  # port ของโฮมฐานข้อมูล
        "SET": "storage_engine=INNODB,character_set_connection=utf8,collation_connection=utf8_unicode_ci",
    }
}

# DBBACKUP_CONNECTORS = {
#     'default': {
#         'USER': 'backupuser',
#         'PASSWORD': 'backuppassword',
#         'HOST': 'replica-for-backup'
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

AUTHENTICATION_BACKENDS = ["django.contrib.auth.backends.AllowAllUsersModelBackend"]

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Bangkok"

USE_I18N = True

USE_L10N = True

USE_TZ = False

LOCALE_PATHS = (os.path.join(BASE_DIR, "locale"),)
LANGUAGES = (("en", _("English")), ("th", _("Thailand")))
# Static files (CSS, JavaScript, Images)
# Srorage save file
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "")]

LOGIN_REDIRECT_URL = "/DigitalBiobankApp/"
LOGIN_URL = "/Users/login/"

# Email protocol
EMAIL_USE_TLS = True
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = "budgetmanage2019a@gmail.com"
EMAIL_HOST_PASSWORD = "Budget2019a"
EMAIL_PORT = 587
