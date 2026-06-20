"""WebSocket-consumers: push обновлений заказов (HTML-фрагменты, HTMX OOB-swap).

Принцип: мутации идут по HTTP, сюда приходит лишь сигнал «изменилось» —
consumer перерисовывает фрагмент на языке своего соединения и шлёт в сокет.
"""
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.template.loader import render_to_string

from apps.core.translations import i18n_context, normalize_lang


class CabinetOrdersConsumer(AsyncWebsocketConsumer):
    """Доска заказов в кабинете. Группа orders.<restaurant_id>."""

    async def connect(self):
        self.user = self.scope.get('user')
        self.slug = self.scope['url_route']['kwargs']['slug']
        if not (self.user and self.user.is_authenticated):
            await self.close()
            return
        ok = await self._load()
        if not ok:
            await self.close()
            return
        self.group = f'orders.{self.restaurant_id}'
        await self.channel_layer.group_add(self.group, self.channel_name)
        await self.accept()
        await self._send_board()  # начальная отрисовка / ресинк при реконнекте

    async def disconnect(self, code):
        if hasattr(self, 'group'):
            await self.channel_layer.group_discard(self.group, self.channel_name)

    async def board_changed(self, event):
        await self._send_board()

    @database_sync_to_async
    def _load(self):
        from apps.restaurants.access import can, membership_for
        from apps.restaurants.models import Restaurant
        r = Restaurant.objects.filter(slug=self.slug).first()
        if r is None:
            return False
        m = membership_for(self.user, r)
        if not can(m, 'orders'):
            return False
        self.restaurant = r
        self.restaurant_id = r.id
        self.membership = m
        self.lang = normalize_lang((self.scope.get('session') or {}).get('lang', 'ru'))
        return True

    @database_sync_to_async
    def _render(self):
        from .views import _board_context
        ctx = {**_board_context(self.restaurant, self.lang, self.membership), **i18n_context(self.lang)}
        html = render_to_string('cabinet/_orders_board.html', ctx)
        return f'<div id="board" hx-swap-oob="innerHTML">{html}</div>'

    async def _send_board(self):
        await self.send(text_data=await self._render())


class GuestOrderConsumer(AsyncWebsocketConsumer):
    """Экран статуса у гостя. Группа order.<order_id>."""

    async def connect(self):
        self.token = self.scope['url_route']['kwargs']['token']
        ok = await self._load()
        if not ok:
            await self.close()
            return
        self.group = f'order.{self.order_id}'
        await self.channel_layer.group_add(self.group, self.channel_name)
        await self.accept()
        await self._send_status()

    async def disconnect(self, code):
        if hasattr(self, 'group'):
            await self.channel_layer.group_discard(self.group, self.channel_name)

    async def order_changed(self, event):
        await self._send_status()

    @database_sync_to_async
    def _load(self):
        from .models import Order
        o = Order.objects.filter(public_token=self.token).first()
        if o is None:
            return False
        self.order_id = o.id
        self.lang = normalize_lang((self.scope.get('session') or {}).get('lang', 'ru'))
        return True

    @database_sync_to_async
    def _render(self):
        from .models import Order
        from .views import _status_steps
        order = Order.objects.prefetch_related('items').get(pk=self.order_id)
        ctx = {
            'order': order,
            'flow': _status_steps(order, self.lang),
            **i18n_context(self.lang),
        }
        html = render_to_string('public/_order_status_inner.html', ctx)
        return f'<div id="order-status" hx-swap-oob="innerHTML">{html}</div>'

    async def _send_status(self):
        await self.send(text_data=await self._render())
