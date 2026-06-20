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


# Пары шрифтов для гостевого меню (display — заголовки, body — текст).
# google — строка для https://fonts.googleapis.com/css2?family=…
FONT_PAIRS = {
    'classic': {'label': 'Классика',     'display': "'Spectral', serif",          'body': "'Golos Text', sans-serif",
                'google': 'Spectral:wght@500;600;700&family=Golos+Text:wght@400;500;600;700'},
    'modern':  {'label': 'Современный',  'display': "'Manrope', sans-serif",       'body': "'Manrope', sans-serif",
                'google': 'Manrope:wght@400;500;600;700;800'},
    'elegant': {'label': 'Элегантный',   'display': "'Playfair Display', serif",   'body': "'Inter', sans-serif",
                'google': 'Playfair+Display:wght@500;600;700&family=Inter:wght@400;500;600'},
    'rounded': {'label': 'Мягкий',       'display': "'Baloo 2', system-ui",        'body': "'Nunito', sans-serif",
                'google': 'Baloo+2:wght@500;600;700&family=Nunito:wght@400;500;600;700'},
}

RADIUS_PX = {'none': 0, 'sm': 8, 'md': 14, 'lg': 22}


def relative_luminance(hex_color):
    """Относительная яркость цвета (WCAG) — для выбора контрастного текста."""
    h = (hex_color or '').lstrip('#')
    if len(h) != 6:
        return 0.0
    try:
        r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    except ValueError:
        return 0.0
    def lin(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


class MenuTheme(models.Model):
    """Оформление публичного меню заведения. Один на заведение.

    Применяется к гостевому меню через CSS-переменные и data-атрибуты —
    структура шаблона одна, вид меняется темой.
    """

    class Card(models.TextChoices):
        LIST = 'list', 'Список с фото'
        GRID = 'grid', 'Плитка'
        COMPACT = 'compact', 'Компактный'

    class Radius(models.TextChoices):
        NONE = 'none', 'Прямые углы'
        SM = 'sm', 'Слегка'
        MD = 'md', 'Средне'
        LG = 'lg', 'Сильно'

    class Header(models.TextChoices):
        LEFT = 'left', 'Слева'
        CENTER = 'center', 'По центру'

    restaurant = models.OneToOneField(
        Restaurant, on_delete=models.CASCADE, related_name='theme', verbose_name='Заведение',
    )
    # цвета
    accent = models.CharField('Акцент', max_length=7, default='#C75B39')
    bg = models.CharField('Фон', max_length=7, default='#FBF6EE')
    text = models.CharField('Текст', max_length=7, default='#2A2118')
    card_bg = models.CharField('Фон карточек', max_length=7, default='#FFFFFF')
    # типографика
    font = models.CharField('Шрифт', max_length=20, default='classic',
                            choices=[(k, v['label']) for k, v in FONT_PAIRS.items()])
    # карточки блюд
    card_style = models.CharField('Стиль карточек', max_length=10, choices=Card.choices, default=Card.LIST)
    radius = models.CharField('Скругление', max_length=6, choices=Radius.choices, default=Radius.LG)
    show_desc = models.BooleanField('Показывать описания', default=True)
    # шапка / логотип
    show_logo = models.BooleanField('Логотип в шапке', default=True)
    header_layout = models.CharField('Шапка', max_length=8, choices=Header.choices, default=Header.LEFT)
    cover = models.ImageField('Обложка', upload_to='restaurants/covers/', blank=True, null=True)

    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    class Meta:
        verbose_name = 'Дизайн меню'
        verbose_name_plural = 'Дизайн меню'

    def __str__(self):
        return f'Тема {self.restaurant}'

    @property
    def font_conf(self):
        return FONT_PAIRS.get(self.font, FONT_PAIRS['classic'])

    @property
    def radius_px(self):
        return RADIUS_PX.get(self.radius, RADIUS_PX['lg'])

    @property
    def header_text(self):
        """Контрастный цвет текста в шапке: тёмный на светлом акценте, иначе белый."""
        return '#2A2118' if relative_luminance(self.accent) > 0.55 else '#FFFFFF'

    @classmethod
    def for_restaurant(cls, restaurant):
        """Сохранённая тема либо дефолтная (несохранённая) — у меню всегда есть тема."""
        return getattr(restaurant, 'theme', None) or cls(restaurant=restaurant)


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


class TableZone(models.Model):
    """Зона/секция заведения: этаж, зал, улица, терраса и т.п.

    Группирует столы. Удаление зоны не трогает столы — они становятся «без зоны».
    """

    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='zones',
        verbose_name='Заведение',
    )
    name = models.CharField('Название', max_length=80)  # «2 этаж», «Улица», «VIP-зал»
    sort_order = models.PositiveIntegerField('Порядок', default=0)
    created_at = models.DateTimeField('Создана', auto_now_add=True)

    class Meta:
        verbose_name = 'Зона'
        verbose_name_plural = 'Зоны'
        ordering = ('sort_order', 'id')

    def __str__(self):
        return self.name


class Table(models.Model):
    """Стол заведения. QR на столе ведёт на меню именно этого стола."""

    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='tables',
        verbose_name='Заведение',
    )
    zone = models.ForeignKey(
        TableZone,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tables',
        verbose_name='Зона',
    )
    name = models.CharField('Название/номер', max_length=50)  # «Стол 12», «Топчан 3»
    qr_token = models.CharField('QR-токен', max_length=32, unique=True, default=gen_qr_token, editable=False)
    # Официанты, закреплённые за столом: видят и ведут только заказы своих столов.
    # Если за столом никого нет — заказ виден всем (общий пул).
    waiters = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='assigned_tables',
        blank=True,
        verbose_name='Официанты',
    )
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
