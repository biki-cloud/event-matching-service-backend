"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 5.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from datetime import timedelta
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-s%dh--yr$zn1o%vf=$ztrvsvvr1g2-=48eg98*(8-mi%5jbbw1"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = ['*']
ALLOWED_HOSTS = [
    '*',
    '.vercel.app'
]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework", # rest frameworkの設定
    'corsheaders', # corsの設定
    "drf_spectacular", # swaggerの設定
    'api.events', # eventsアプリケーションの設定
    'api.accounts', # accountsアプリケーションの設定
    'rest_framework.authtoken', # rest frameworkのトークン認証
    'djoser', # djoser(認証系)の設定
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'corsheaders.middleware.CorsMiddleware', # corsの設定
    'django.middleware.common.CommonMiddleware', # corsの設定
]

ROOT_URLCONF = "config.urls"

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',  # Next.jsの開発サーバーのURL
    'http://127.0.0.1:3000',  # Next.jsの開発サーバーのURL
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "ja-jp"

TIME_ZONE = "Asia/Tokyo"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['console'],
        }
    }
}


# すべてのオリジンを許可する設定(開発時のみ)
CORS_ALLOW_ALL_ORIGINS = True
# CORS許可設定(本番環境用)
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:3000",
# ]

# Swagger設定
SPECTACULAR_SETTINGS = {
    'TITLE': 'プロジェクト名',
    'DESCRIPTION': '詳細',
    'VERSION': '1.0.0',
    # api/schemaを表示しない
    'SERVE_INCLUDE_SCHEMA': False,
}

STATIC_ROOT = os.path.join(BASE_DIR, 'static')


# メール設定
# 開発環境
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# 本番環境
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'メールアドレス'
# EMAIL_HOST_PASSWORD = 'パスワード'
# DEFAULT_FROM_EMAIL = 'メールアドレス'


REST_FRAMEWORK = {
    # 認証が必要
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema', # swagger設定
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    'AUTH_HEADER_TYPES': ('JWT',),
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
}

DJOSER = {
    # メールアドレスでログイン
    'LOGIN_FIELD': 'email',
    # アカウント本登録メール
    'SEND_ACTIVATION_EMAIL': True,
    # アカウント本登録完了メール
    'SEND_CONFIRMATION_EMAIL': True,
    # メールアドレス変更完了メール
    'USERNAME_CHANGED_EMAIL_CONFIRMATION': True,
    # パスワード変更完了メール
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION': True,
    # アカウント登録時に確認用パスワード必須
    'USER_CREATE_PASSWORD_RETYPE': True,
    # メールアドレス変更時に確認用メールアドレス必須
    'SET_USERNAME_RETYPE': True,
    # パスワード変更時に確認用パスワード必須
    'SET_PASSWORD_RETYPE': True,
    # アカウント本登録用URL
    'ACTIVATION_URL': 'activate/{uid}/{token}',
    # メールアドレスリセット完了用URL
    'USERNAME_RESET_CONFIRM_URL': 'email/reset/confirm/{uid}/{token}',
    # パスワードリセット完了用URL
    'PASSWORD_RESET_CONFIRM_URL': 'password/reset/confirm/{uid}/{token}',
    # カスタムユーザー用シリアライザー
    'SERIALIZERS': {
        'user_create': 'api.accounts.serializers.UserSerializer',
        'user': 'api.accounts.serializers.UserSerializer',
        'current_user': 'api.accounts.serializers.UserSerializer',
    },
    'EMAIL': {
        # アカウント本登録
        'activation': 'api.accounts.email.ActivationEmail',
        # アカウント本登録完了
        'confirmation': 'api.accounts.email.ConfirmationEmail',
        # パスワードリセット
        'password_reset': 'api.accounts.email.PasswordResetEmail',
        # パスワードリセット完了
        'password_changed_confirmation': 'api.accounts.email.PasswordChangedConfirmationEmail',
        # メールアドレスリセット
        'username_reset': 'api.accounts.email.UsernameResetEmail',
        # メールアドレスリセット完了
        'username_changed_confirmation': 'api.accounts.email.UsernameChangedConfirmationEmail',
    },
}

AUTH_USER_MODEL = 'accounts.UserAccount'