from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone


def normalize_phone(phone):
    """Привести телефон к виду +998XXXXXXXXX (только «+» и цифры)."""
    if not phone:
        return phone
    return '+' + ''.join(ch for ch in str(phone) if ch.isdigit())


def is_valid_uz_phone(phone):
    """Узбекский мобильный: +998 и ровно 9 цифр (всего 12 цифр)."""
    import re
    return bool(re.fullmatch(r'\+998\d{9}', normalize_phone(phone) or ''))


# Лимиты тарифов (None = без ограничений). Соответствуют лендингу.
PLAN_LIMITS = {
    'start':    {'venues': 1,    'dishes': 30},
    'business': {'venues': 3,    'dishes': None},
    'network':  {'venues': None, 'dishes': None},
}


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, phone, password, **extra_fields):
        if not phone:
            raise ValueError('Номер телефона обязателен')
        user = self.model(phone=normalize_phone(phone), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone, password, **extra_fields)

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')
        return self._create_user(phone, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Пользователь платформы. Идентификатор входа — телефон +998."""

    class Plan(models.TextChoices):
        START = 'start', 'Старт'
        BUSINESS = 'business', 'Бизнес'
        NETWORK = 'network', 'Сеть'

    phone = models.CharField('Телефон', max_length=20, unique=True)
    full_name = models.CharField('Имя', max_length=150, blank=True)
    # Тариф владельца: ограничивает число его заведений и блюд в них.
    # Меняется вручную/в админке — оплата подключается отдельно.
    plan = models.CharField('Тариф', max_length=20, choices=Plan.choices, default=Plan.START)
    # Агент — сотрудник, который подключает заведения (заводит им аккаунты).
    # Только агенты (и суперпользователь) создают новые заведения.
    is_agent = models.BooleanField('Агент', default=False)
    is_active = models.BooleanField('Активен', default=True)
    is_staff = models.BooleanField('Доступ в админку', default=False)
    date_joined = models.DateTimeField('Дата регистрации', default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.full_name or self.phone

    @property
    def venue_limit(self):
        """Сколько заведений можно иметь (None = без лимита)."""
        return PLAN_LIMITS.get(self.plan, PLAN_LIMITS['start'])['venues']

    @property
    def dish_limit(self):
        """Сколько блюд можно в одном заведении (None = без лимита)."""
        return PLAN_LIMITS.get(self.plan, PLAN_LIMITS['start'])['dishes']

    @property
    def venues_used(self):
        return self.owned_restaurants.count()

    @property
    def can_add_venue(self):
        limit = self.venue_limit
        return limit is None or self.venues_used < limit

    @property
    def is_agent_user(self):
        """Может заводить заведения: агент или суперпользователь."""
        return bool(self.is_agent or self.is_superuser)


class Lead(models.Model):
    """Заявка с лендинга «Оставить заявку» (самостоятельной регистрации нет).
    Менеджер/агент перезванивает и подключает заведение вручную."""

    full_name = models.CharField('Имя', max_length=150, blank=True)
    phone = models.CharField('Телефон', max_length=20)
    venue_name = models.CharField('Заведение', max_length=150, blank=True)
    city = models.CharField('Город', max_length=80, blank=True)
    comment = models.TextField('Комментарий', blank=True)
    is_processed = models.BooleanField('Обработана', default=False)
    created_at = models.DateTimeField('Создана', auto_now_add=True)

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.venue_name or self.full_name} · {self.phone}'


class PhoneOTP(models.Model):
    """Одноразовый код подтверждения телефона (вход/регистрация по SMS)."""

    phone = models.CharField('Телефон', max_length=20, db_index=True)
    code = models.CharField('Код', max_length=6)
    is_used = models.BooleanField('Использован', default=False)
    attempts = models.PositiveSmallIntegerField('Попыток', default=0)
    created_at = models.DateTimeField('Создан', auto_now_add=True)

    class Meta:
        verbose_name = 'SMS-код'
        verbose_name_plural = 'SMS-коды'
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.phone} · {self.code}'
