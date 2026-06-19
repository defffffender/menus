"""Публикация realtime-событий в channel layer.

Шлём лёгкий сигнал (без HTML) — каждый consumer перерисует фрагмент на своём
языке. Группы: `orders.<restaurant_id>` (кабинет), `order.<order_id>` (гость).
"""
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def cabinet_group(restaurant_id):
    return f'orders.{restaurant_id}'


def order_group(order_id):
    return f'order.{order_id}'


def notify_order_change(order):
    """Сообщить кабинету заведения и гостю заказа, что заказ изменился."""
    layer = get_channel_layer()
    if layer is None:
        return
    async_to_sync(layer.group_send)(cabinet_group(order.restaurant_id), {'type': 'board.changed'})
    async_to_sync(layer.group_send)(order_group(order.id), {'type': 'order.changed'})
