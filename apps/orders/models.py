import uuid

from django.db import models

from apps.menu.models import DishVariant
from apps.restaurants.models import Restaurant, Table


def gen_order_token():
    return uuid.uuid4().hex


class Order(models.Model):
    """Заказ гостя за столом. Дозаказ — это новый отдельный Order на тот же стол."""

    class Status(models.TextChoices):
        NEW = 'new', 'Новый'
        ACCEPTED = 'accepted', 'Принят'
        COOKING = 'cooking', 'Готовится'
        SERVED = 'served', 'Подан'
        CLOSED = 'closed', 'Закрыт'
        CANCELLED = 'cancelled', 'Отменён'

    # Активные статусы (видны на доске кабинета), в порядке продвижения.
    FLOW = (Status.NEW, Status.ACCEPTED, Status.COOKING, Status.SERVED)

    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name='orders', verbose_name='Заведение',
    )
    table = models.ForeignKey(
        Table, on_delete=models.SET_NULL, null=True, related_name='orders', verbose_name='Стол',
    )
    status = models.CharField('Статус', max_length=12, choices=Status.choices, default=Status.NEW)
    comment = models.TextField('Комментарий гостя', blank=True)
    # Токен для гостя — смотреть статус без регистрации.
    public_token = models.CharField('Токен', max_length=32, unique=True, default=gen_order_token, editable=False)

    created_at = models.DateTimeField('Создан', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлён', auto_now=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ('-created_at',)

    def __str__(self):
        return f'Заказ №{self.pk}'

    @property
    def total(self):
        return sum(i.line_total for i in self.items.all())

    @property
    def is_active(self):
        return self.status in self.FLOW

    def next_status(self):
        """Следующий статус по цепочке Новый→Принят→Готовится→Подан→Закрыт."""
        chain = list(self.FLOW) + [self.Status.CLOSED]
        if self.status in chain:
            i = chain.index(self.status)
            if i + 1 < len(chain):
                return chain[i + 1]
        return None


class OrderItem(models.Model):
    """Позиция заказа. Название и цена — снимок на момент заказа."""

    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='items', verbose_name='Заказ',
    )
    # Ссылка для аналитики; цена/название берём из снимка ниже.
    variant = models.ForeignKey(
        DishVariant, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Вариант',
    )
    name = models.CharField('Название (снимок)', max_length=240)
    price = models.PositiveIntegerField('Цена (снимок)')
    quantity = models.PositiveSmallIntegerField('Количество', default=1)

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказа'

    def __str__(self):
        return f'{self.name} ×{self.quantity}'

    @property
    def line_total(self):
        return self.price * self.quantity
