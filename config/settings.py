"""
MindSkills BrainGames — Django (MVT) sozlamalari.

Bolalar uchun aqliy ko'nikmalarni rivojlantiruvchi o'yin platformasi:
mental arifmetika, abakus (soroban) va tez o'qish. O'zbek tilida,
adaptiv qiyinlik tizimi va ota-ona nazorati bilan.
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# --- Asosiy / xavfsizlik ------------------------------------------------------
# PythonAnywhere'da quyidagi qiymatlarni atrof-muhit (environment) orqali bering.
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure--gc2b^!@*1*!o4pn9t-7_5ty(^=a8$a!kf+27)9x60v78wc+d#",
)

# Ishlab chiqarish (production) — standart holatda DEBUG o'chiq.
# Lokal ishlash uchun: DJANGO_DEBUG=True qo'ying.
DEBUG = os.environ.get("DJANGO_DEBUG", "False") == "True"

# Barcha hostlarga ruxsat (PythonAnywhere uchun). Kerak bo'lsa
# DJANGO_ALLOWED_HOSTS bilan aniq domenlarni bering.
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "*").split(",")

# DEBUG=False bo'lganda forma (POST) ishlashi uchun ishonchli manbalar.
# O'z domeningiz bo'lsa, DJANGO_CSRF_TRUSTED bilan qo'shing.
CSRF_TRUSTED_ORIGINS = os.environ.get(
    "DJANGO_CSRF_TRUSTED",
    "https://*.pythonanywhere.com",
).split(",")

# --- Production xavfsizligi (ixtiyoriy, HTTPS ortida) -------------------------
# PythonAnywhere'da WSGI faylida DJANGO_SECURE=True qo'ysangiz yoqiladi.
# (Standart holatda o'chiq — lokal/HTTP test buzilmasligi uchun.)
if os.environ.get("DJANGO_SECURE") == "True":
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    X_FRAME_OPTIONS = "DENY"
    # HSTS — brauzerga "doim HTTPS ishlat" deydi (1 yil). Faqat HTTPS
    # production'da yoqing (DJANGO_SECURE=True), aks holda domeningiz
    # HTTPS'siz ochilmay qoladi.
    SECURE_HSTS_SECONDS = int(os.environ.get("DJANGO_HSTS_SECONDS", "31536000"))
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# --- Ilovalar -----------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Loyiha ilovalari
    "accounts",
    "games",
    "core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.site_context",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# --- Ma'lumotlar bazasi -------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# --- Parol tekshiruvchilari ---------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 6},
    },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
]

# --- Til / vaqt ---------------------------------------------------------------
LANGUAGE_CODE = "uz"
TIME_ZONE = "Asia/Tashkent"
USE_I18N = True
USE_TZ = True

LANGUAGES = [
    ("uz", "O'zbekcha"),
]

# --- Statik va media fayllar --------------------------------------------------
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- Autentifikatsiya ---------------------------------------------------------
AUTH_USER_MODEL = "accounts.User"
LOGIN_URL = "accounts:login"
LOGIN_REDIRECT_URL = "core:home"
LOGOUT_REDIRECT_URL = "accounts:login"

MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"

# --- Email (ota-ona nazorati tasdig'i) ---------------------------------------
# Dev: konsolga chiqadi. Haqiqiy Gmail uchun env o'zgaruvchilarni bering:
#   DJANGO_EMAIL_HOST_USER, DJANGO_EMAIL_HOST_PASSWORD (Gmail App Password)
if os.environ.get("DJANGO_EMAIL_HOST_USER"):
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = os.environ.get("DJANGO_EMAIL_HOST", "smtp.gmail.com")
    EMAIL_PORT = int(os.environ.get("DJANGO_EMAIL_PORT", "587"))
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = os.environ.get("DJANGO_EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = os.environ.get("DJANGO_EMAIL_HOST_PASSWORD", "")
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    DEFAULT_FROM_EMAIL = "BrainGames <noreply@braingames.uz>"
