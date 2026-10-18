from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env
try:
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR / '.env')
except ImportError:
    pass

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')

SECRET_KEY = 'django-insecure-boutique-fashion-shop-key-2024-change-in-production'

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'store',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'shopquanao.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'store.context_processors.shop_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'shopquanao.wsgi.application'

try:
    import dj_database_url
except ImportError:
    dj_database_url = None

DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL and dj_database_url:
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'vi'
TIME_ZONE = 'Asia/Ho_Chi_Minh'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ============================================================
# JAZZMIN ADMIN SETTINGS (Giao diện Quản trị Chuyên Nghiệp)
# ============================================================
JAZZMIN_SETTINGS = {
    "site_title": "Shop Hồng Loan Admin",
    "site_header": "Shop Hồng Loan",
    "site_brand": "Shop Hồng Loan",
    "welcome_sign": "Chào mừng đến với Hệ thống Quản trị Shop Hồng Loan",
    "copyright": "Shop Hồng Loan",
    "search_model": ["store.Product", "store.Order"],

    "topmenu_links": [
        {"name": "Trang chủ Shop ↗", "url": "/", "new_window": True},
        {"model": "store.Order"},
        {"model": "store.Product"},
        {"model": "store.ShopSetting"},
    ],

    "usermenu_links": [
        {"name": "Xem Cửa Hàng ↗", "url": "/", "new_window": True},
    ],

    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],

    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "store.Product": "fas fa-tshirt",
        "store.Category": "fas fa-tags",
        "store.Order": "fas fa-shopping-cart",
        "store.Banner": "fas fa-images",
        "store.ShopSetting": "fas fa-phone-alt",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",

    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {"auth.user": "collapsible", "auth.group": "vertical_tabs"},
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-dark",
    "accent": "accent-warning",
    "navbar": "navbar-dark navbar-navy",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-warning",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "flatly",
    "default_theme_mode": "light",
    "button_classes": {
        "primary": "btn-outline-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}
