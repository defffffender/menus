"""Сервис-слой заказов: запись в БД + публикация realtime-события.

Уведомляем через `transaction.on_commit` — событие уходит только после фиксации,
чтобы consumer, перечитывая БД, увидел уже сохранённое состояние.
"""
from django.db import transaction

from .models import Order, OrderItem
from .realtime import notify_order_change


@transaction.atomic
def place_order(restaurant, table, comment, items):
    """Создать заказ со статусом «Новый». `items` — список несохранённых OrderItem."""
    order = Order.objects.create(restaurant=restaurant, table=table, comment=comment)
    for it in items:
        it.order = order
    OrderItem.objects.bulk_create(items)
    transaction.on_commit(lambda: notify_order_change(order))
    return order


@transaction.atomic
def apply_status_action(order, action):
    """Сменить статус: 'advance' (по цепочке) или 'cancel'. Возвращает True, если изменилось."""
    changed = False
    if action == 'cancel':
        order.status = Order.Status.CANCELLED
        changed = True
    elif action == 'advance':
        nxt = order.next_status()
        if nxt:
            order.status = nxt
            changed = True
    if changed:
        order.save(update_fields=['status', 'updated_at'])
        transaction.on_commit(lambda: notify_order_change(order))
    return changed
