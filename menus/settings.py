
from pathlib import Path

import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Конфиг из окружения (12-factor). Значения по умолчанию — для разработки;
# на проде задаются через .env / переменные окружения.
env = environ.Env(
    DEBUG=(bool, True),
    SECRET_KEY=(str, 'django-insecure-%!6h5t86lo0f&0o1_i@i=$2g*wu%86ba_n-a6^+*%$qcqzx!1y'),
    ALLOWED_HOSTS=(list, []),
    CSRF_TRUSTED_ORIGINS=(list, []),
    REDIS_URL=(str, ''),
)
# .env читаем, если есть (на проде); в dev можно без файла.
environ.Env.read_env(BASE_DIR / '.env')

DEBUG = env('DEBUG')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# В разработке разрешаем любой хост (чтобы открыть с телефона по IP в той же
# Wi-Fi-сети). На проде ALLOWED_HOSTS задаётся явно через окружение.
ALLOWED_HOSTS = ['*'] if DEBUG else env('ALLOWED_HOSTS')

# Для WS/POST через HTTPS с домена (прод): https://menu.example.uz
CSRF_TRUSTED_ORIGINS = env('CSRF_TRUSTED_ORIGINS')


# Application definition

INSTALLED_APPS = [
    # daphne должен быть выше staticfiles — даёт ASGI-runserver (WebSocket в dev)
    'daphne',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # realtime
    'channels',

    # local apps
    'apps.core',
    'apps.accounts',
    'apps.restaurants',
    'apps.menu',
    'apps.orders',
]

AUTH_USER_MODEL = 'accounts.User'

LOGIN_URL = '/login/'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'menus.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.core.context_processors.i18n',
            ],
        },
    },
]

WSGI_APPLICATION = 'menus.wsgi.application'
ASGI_APPLICATION = 'menus.asgi.application'

# Channel layer: на проде — Redis (общие WS-группы между воркерами/серверами),
# в разработке — InMemory (без внешних сервисов, один процесс).
if env('REDIS_URL'):
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels_redis.core.RedisChannelLayer',
            'CONFIG': {'hosts': [env('REDIS_URL')]},
        },
    }
else:
    CHANNEL_LAYERS = {
        'default': {'BACKEND': 'channels.layers.InMemoryChannelLayer'},
    }


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Asia/Tashkent'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = 'static/'

# Media (загружаемые файлы: логотипы, фото блюд)
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Ограничение тела запроса (защита от слишком больших POST; файлы валидируются
# отдельно в формах — до 5 МБ на картинку).
DATA_UPLOAD_MAX_MEMORY_SIZE = 6 * 1024 * 1024

# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
