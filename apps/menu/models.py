from django.db import models

from apps.restaurants.models import Restaurant


class Category(models.Model):
    """Раздел меню (Салаты, Горячее, Напитки). Название на трёх языках."""

    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='categories',
        verbose_name='Заведение',
    )
    name_ru = models.CharField('Название (RU)', max_length=120)
    name_uz = models.CharField('Название (UZ)', max_length=120, blank=True)
    name_en = models.CharField('Название (EN)', max_length=120, blank=True)

    sort_order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активен', default=True)
    created_at = models.DateTimeField('Создан', auto_now_add=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('sort_order', 'id')

    def __str__(self):
        return self.name_ru

    def name(self, lang='ru'):
        return getattr(self, f'name_{lang}', '') or self.name_ru


class Dish(models.Model):
    """Блюдо. Фото обязательно. Цены живут в вариантах (`DishVariant`)."""

    class Spiciness(models.IntegerChoices):
        NONE = 0, 'Не острое'
        MILD = 1, 'Слабо острое'
        SPICY = 2, 'Острое'
        HOT = 3, 'Очень острое'

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='dishes',
        verbose_name='Категория',
    )
    name_ru = models.CharField('Название (RU)', max_length=150)
    name_uz = models.CharField('Название (UZ)', max_length=150, blank=True)
    name_en = models.CharField('Название (EN)', max_length=150, blank=True)

    description_ru = models.TextField('Описание (RU)', blank=True)
    description_uz = models.TextField('Описание (UZ)', blank=True)
    description_en = models.TextField('Описание (EN)', blank=True)

    # Фото обязательно (требование проекта).
    photo = models.ImageField('Фото', upload_to='dishes/')

    # Доп. атрибуты.
    weight = models.CharField('Вес/объём', max_length=40, blank=True)  # «250 г», «0.5 л»
    spiciness = models.PositiveSmallIntegerField(
        'Острота', choices=Spiciness.choices, default=Spiciness.NONE,
    )
    prep_time = models.PositiveSmallIntegerField('Время (мин)', null=True, blank=True)

    is_available = models.BooleanField('В наличии', default=True)  # стоп-лист
    sort_order = models.PositiveIntegerField('Порядок', default=0)
    created_at = models.DateTimeField('Создано', auto_now_add=True)

    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'
        ordering = ('sort_order', 'id')

    def __str__(self):
        return self.name_ru

    def name(self, lang='ru'):
        return getattr(self, f'name_{lang}', '') or self.name_ru

    @property
    def min_price(self):
        prices = [v.price for v in self.variants.all()]
        return min(prices) if prices else None

    @property
    def has_variants(self):
        # len(...) использует prefetch-кэш (variants уже подгружены в списке меню),
        # тогда как .count() делал бы лишний запрос на каждое блюдо.
        return len(self.variants.all()) > 1


class DishVariant(models.Model):
    """Вариант/размер блюда с ценой (целое, сумы). У блюда минимум один."""

    dish = models.ForeignKey(
        Dish,
        on_delete=models.CASCADE,
        related_name='variants',
        verbose_name='Блюдо',
    )
    name_ru = models.CharField('Вариант (RU)', max_length=80, blank=True)  # «Обычная», «Большая»
    name_uz = models.CharField('Вариант (UZ)', max_length=80, blank=True)
    name_en = models.CharField('Вариант (EN)', max_length=80, blank=True)
    price = models.PositiveIntegerField('Цена (сум)')

    sort_order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Вариант блюда'
        verbose_name_plural = 'Варианты блюда'
        ordering = ('sort_order', 'id')

    def __str__(self):
        return f'{self.dish.name_ru} — {self.name_ru or "—"} ({self.price})'

    def name(self, lang='ru'):
        return getattr(self, f'name_{lang}', '') or self.name_ru
