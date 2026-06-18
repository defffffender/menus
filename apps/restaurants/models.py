import uuid

from django.conf import settings
from django.db import models


def gen_qr_token():
    return uuid.uuid4().hex


class Restaurant(models.Model):
    """Заведение — арендатор (тенант) платформы."""

    class Type(models.TextChoices):
        RESTAURANT = 'restaurant', 'Ресторан'
        CAFE = 'cafe', 'Кафе'
        CHAIKHANA = 'chaikhana', 'Чайхана'
        FASTFOOD = 'fastfood', 'Фастфуд'

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='owned_restaurants',
        verbose_name='Владелец',
    )
    # Бренд-имя обычно не переводят, поэтому одно поле.
    name = models.CharField('Название', max_length=150)
    # slug адресует тенанта по пути (menus.uz/r/<slug>); тот же slug подойдёт
    # для поддомена <slug>.menus.uz в будущем без миграции данных.
    slug = models.SlugField('Адрес (slug)', max_length=60, unique=True, allow_unicode=True)
    type = models.CharField('Тип', max_length=20, choices=Type.choices, default=Type.RESTAURANT)
    city = models.CharField('Город', max_length=80, blank=True)
    phone = models.CharField('Телефон', max_length=20, blank=True)
    logo = models.ImageField('Логотип', upload_to='restaurants/logos/', blank=True, null=True)

    # Описание для витрины — на трёх языках.
    description_ru = models.TextField('Описание (RU)', blank=True)
    description_uz = models.TextField('Описание (UZ)', blank=True)
    description_en = models.TextField('Описание (EN)', blank=True)

    is_active = models.BooleanField('Активно', default=True)
    created_at = models.DateTimeField('Создано', auto_now_add=True)

    class Meta:
        verbose_name = 'Заведение'
        verbose_name_plural = 'Заведения'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Membership(models.Model):
    """Связь сотрудника с заведением и его роль (гибкая RBAC-модель)."""

    class Role(models.TextChoices):
        OWNER = 'owner', 'Владелец'
        DIRECTOR = 'director', 'Директор'
        ADMINISTRATOR = 'administrator', 'Управляющий'
        MANAGER = 'manager', 'Менеджер'
        WAITER = 'waiter', 'Официант'
        KITCHEN = 'kitchen', 'Кухня'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='memberships',
        verbose_name='Сотрудник',
    )
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='memberships',
        verbose_name='Заведение',
    )
    role = models.CharField('Роль', max_length=20, choices=Role.choices)
    is_active = models.BooleanField('Активен', default=True)
    created_at = models.DateTimeField('Добавлен', auto_now_add=True)

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'restaurant'),
                name='unique_user_per_restaurant',
            ),
        ]

    def __str__(self):
        return f'{self.user} — {self.get_role_display()} @ {self.restaurant}'


class Table(models.Model):
    """Стол заведения. QR на столе ведёт на меню именно этого стола."""

    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='tables',
        verbose_name='Заведение',
    )
    name = models.CharField('Название/номер', max_length=50)  # «Стол 12», «Топчан 3»
    qr_token = models.CharField('QR-токен', max_length=32, unique=True, default=gen_qr_token, editable=False)
    seats = models.PositiveSmallIntegerField('Мест', null=True, blank=True)
    is_active = models.BooleanField('Активен', default=True)
    sort_order = models.PositiveIntegerField('Порядок', default=0)
    created_at = models.DateTimeField('Создан', auto_now_add=True)

    class Meta:
        verbose_name = 'Стол'
        verbose_name_plural = 'Столы'
        ordering = ('sort_order', 'id')

    def __str__(self):
        return self.name
