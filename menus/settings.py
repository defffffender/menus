
from datetime import timedelta
from pathlib import Path

import environ
from django.templatetags.static import static

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

    # современная тема админки (обязательно ДО django.contrib.admin)
    'unfold',
    'unfold.contrib.filters',
    'unfold.contrib.forms',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # realtime
    'channels',

    # защита логина/админки от перебора пароля
    'axes',

    # local apps
    'apps.core',
    'apps.accounts',
    'apps.restaurants',
    'apps.menu',
    'apps.orders',
]

AUTH_USER_MODEL = 'accounts.User'

# ===== Внешний вид админки (django-unfold) =====
# Логика админки не меняется — только оформление в фирменной палитре Menus.
UNFOLD = {
    'SITE_TITLE': 'Menus admin',
    'SITE_HEADER': 'Menus',
    'SITE_SUBHEADER': 'Платформа · панель управления',
    'SITE_SYMBOL': 'storefront',
    'SITE_FAVICONS': [
        {'rel': 'icon', 'type': 'image/svg+xml', 'href': lambda request: static('favicon.svg')},
        {'rel': 'icon', 'sizes': '32x32', 'type': 'image/png', 'href': lambda request: static('favicon-32.png')},
        {'rel': 'apple-touch-icon', 'href': lambda request: static('apple-touch-icon.png')},
    ],
    'SHOW_HISTORY': True,
    'SHOW_VIEW_ON_SITE': False,
    'COLORS': {
        # фирменный «глиняно-оранжевый» #C75B39 как primary
        'primary': {
            '50': '251 241 236',
            '100': '246 224 214',
            '200': '236 194 174',
            '300': '224 160 132',
            '400': '214 126 92',
            '500': '199 91 57',
            '600': '177 78 48',
            '700': '147 64 38',
            '800': '118 52 31',
            '900': '94 43 27',
            '950': '52 22 13',
        },
    },
}

LOGIN_URL = '/login/'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'apps.restaurants.middleware.SubscriptionMiddleware',
    # должен идти последним: ловит блокировку перебора и отдаёт ответ-локаут
    'axes.middleware.AxesMiddleware',
]

# Бэкенды аутентификации: Axes идёт первым — на залоченной паре IP+логин он
# прерывает вход (PermissionDenied), иначе пропускает к обычному ModelBackend.
AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesStandaloneBackend',
    'django.contrib.auth.backends.ModelBackend',
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
# По умолчанию SQLite (dev). На проде можно переключить на PostgreSQL, задав
# DATABASE_URL=postgres://user:pass@host:5432/dbname в .env (нужен psycopg).

DATABASES = {
    'default': env.db_url(
        'DATABASE_URL',
        default=f'sqlite:///{(BASE_DIR / "db.sqlite3").as_posix()}',
    ),
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
# Куда collectstatic собирает статику для отдачи nginx-ом на проде.
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media (загружаемые файлы: логотипы, фото блюд)
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Ограничение тела запроса (защита от слишком больших POST; файлы валидируются
# отдельно в формах — до 5 МБ на картинку).
DATA_UPLOAD_MAX_MEMORY_SIZE = 6 * 1024 * 1024

# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# --- Безопасность на проде (DEBUG=False) ------------------------------------
# Включается только когда DEBUG выключен, чтобы не мешать локальной разработке.
# Рассчитано на схему: nginx терминирует HTTPS и проксирует на daphne по HTTP.
if not DEBUG:
    # доверяем заголовку от nginx, что исходный запрос был по HTTPS
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    # редирект HTTP→HTTPS. Если разворачиваете по IP без TLS — выключите в .env
    SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', default=True)
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    # HSTS: заставляет браузер ходить только по HTTPS. Начнём с 30 дней.
    SECURE_HSTS_SECONDS = env.int('SECURE_HSTS_SECONDS', default=60 * 60 * 24 * 30)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    # За nginx реальный IP клиента — в X-Forwarded-For (1 прокси). Нужно axes,
    # чтобы лочить настоящий IP, а не адрес nginx.
    AXES_IPWARE_PROXY_COUNT = 1
    AXES_IPWARE_META_PRECEDENCE_ORDER = ['HTTP_X_FORWARDED_FOR', 'REMOTE_ADDR']


# --- Кэш --------------------------------------------------------------------
# На проде — Redis (общий для всех воркеров Daphne); в dev — локальная память.
if env('REDIS_URL'):
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.redis.RedisCache',
            'LOCATION': env('REDIS_URL'),
        },
    }


# --- Защита от перебора пароля (django-axes) --------------------------------
# 5 неудачных попыток на пару «IP + телефон» → локаут на 30 минут. Лочим именно
# пару, а не только логин, чтобы атакующий не мог заблокировать чужой аккаунт.
# Хендлер — БД (таблица попыток общая для всех воркеров, состояние не теряется).
AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = timedelta(minutes=30)
AXES_LOCKOUT_PARAMETERS = [['ip_address', 'username']]
AXES_RESET_ON_SUCCESS = True
AXES_LOCKOUT_TEMPLATE = 'accounts/lockout.html'


# Логин в кабинет шлёт поле 'phone', админка — 'username'. Берём из переданных
# в authenticate() реквизитов, иначе из POST любого из полей.
def axes_username(request, credentials):
    if credentials and credentials.get('username'):
        return credentials['username']
    return (request.POST.get('phone') or request.POST.get('username') or '').strip() or None


AXES_USERNAME_CALLABLE = axes_username


# --- Логирование ------------------------------------------------------------
# Пишем в консоль (stdout) — systemd/journald на проде это подхватит.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {'format': '{asctime} {levelname} {name}: {message}', 'style': '{'},
    },
    'handlers': {
        'console': {'class': 'logging.StreamHandler', 'formatter': 'simple'},
    },
    'root': {'handlers': ['console'], 'level': 'INFO'},
    'loggers': {
        'django': {'handlers': ['console'], 'level': 'INFO', 'propagate': False},
        # код подтверждения и ошибки Eskiz
        'sms': {'handlers': ['console'], 'level': 'INFO', 'propagate': False},
    },
}


# --- SMS (Eskiz.uz) ---------------------------------------------------------
# Пока ESKIZ_ENABLED=False — код подтверждения пишется в лог/консоль (dev).
# На проде включаем и задаём логин/пароль кабинета Eskiz через .env.
ESKIZ_ENABLED = env.bool('ESKIZ_ENABLED', default=False)
ESKIZ_EMAIL = env.str('ESKIZ_EMAIL', default='')
ESKIZ_PASSWORD = env.str('ESKIZ_PASSWORD', default='')
# Отправитель: '4546' — тестовый по умолчанию; брендовый ник («Menus») нужно
# отдельно зарегистрировать и промодерировать в кабинете Eskiz.
ESKIZ_FROM = env.str('ESKIZ_FROM', default='4546')
ESKIZ_BASE_URL = env.str('ESKIZ_BASE_URL', default='https://notify.eskiz.uz/api')
