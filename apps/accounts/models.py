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

    phone = models.CharField('Телефон', max_length=20, unique=True)
    full_name = models.CharField('Имя', max_length=150, blank=True)
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
