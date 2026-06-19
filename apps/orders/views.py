import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from apps.core.translations import resolve_lang
from apps.core.translations import t as translate
from apps.menu.models import DishVariant
from apps.restaurants.models import Table
from apps.restaurants.views import _get_restaurant, _shell

from .models import Order, OrderItem
from .services import apply_status_action, place_order


# --- гость ------------------------------------------------------------------

@require_POST
def create_order(request, qr_token):
    """Гость отправляет корзину → создаётся заказ со статусом «Новый»."""
    table = get_object_or_404(
        Table.objects.select_related('restaurant'), qr_token=qr_token, is_active=True,
    )
    restaurant = table.restaurant

    try:
        payload = json.loads(request.body or '{}')
        rows = payload.get('items', [])
        comment = (payload.get('comment') or '').strip()[:500]
    except (ValueError, AttributeError):
        return JsonResponse({'ok': False, 'error': 'bad_request'}, status=400)

    # собираем валидные позиции (вариант принадлежит этому заведению и доступен)
    wanted = {}
    for row in rows:
        try:
            vid = int(row.get('id'))
            qty = int(row.get('qty'))
        except (TypeError, ValueError):
            continue
        if qty < 1:
            continue
        wanted[vid] = wanted.get(vid, 0) + min(qty, 99)

    if not wanted:
        return JsonResponse({'ok': False, 'error': 'empty'}, status=400)

    variants = (
        DishVariant.objects
        .select_related('dish')
        .filter(pk__in=wanted.keys(), dish__category__restaurant=restaurant, dish__is_available=True)
    )

    items = []
    for v in variants:
        qty = wanted[v.pk]
        name = v.dish.name_ru
        if v.name_ru:
            name = f'{name} · {v.name_ru}'
        items.append(OrderItem(variant=v, name=name, price=v.price, quantity=qty))

    if not items:
        return JsonResponse({'ok': False, 'error': 'unavailable'}, status=400)

    order = place_order(restaurant, table, comment, items)

    return JsonResponse({
        'ok': True,
        'redirect': reverse('orders:status', args=[order.public_token]),
    })


def order_status(request, token):
    """Экран статуса заказа для гостя (без регистрации, по токену)."""
    order = get_object_or_404(
        Order.objects.select_related('table', 'restaurant').prefetch_related('items'),
        public_token=token,
    )
    return render(request, 'public/order_status.html', {
        'order': order,
        'restaurant': order.restaurant,
        'table': order.table,
        'flow': _status_steps(order, resolve_lang(request)),
    })


def order_status_poll(request, token):
    """HTMX-фрагмент статуса (резервный опрос гостем, если нет WS)."""
    order = get_object_or_404(Order, public_token=token)
    return render(request, 'public/_order_status.html', {
        'order': order,
        'flow': _status_steps(order, resolve_lang(request)),
    })


def _status_steps(order, lang):
    """Шкала статусов для гостя: пройденные/текущий/будущие."""
    if order.status == Order.Status.CANCELLED:
        return [{'key': 'cancelled', 'label': translate(lang, 'st_cancelled'),
                 'done': True, 'current': True, 'cancelled': True}]
    chain = list(Order.FLOW) + [Order.Status.CLOSED]
    cur = chain.index(order.status) if order.status in chain else -1
    steps = []
    for i, st in enumerate(chain):
        steps.append({
            'key': st,
            'label': translate(lang, f'st_{st}'),
            'done': i <= cur,
            'current': i == cur,
            'cancelled': False,
        })
    return steps


# --- кабинет ----------------------------------------------------------------

@login_required
def orders(request, slug):
    """Доска заказов (страница-оболочка; содержимое грузится HTMX-опросом)."""
    restaurant = _get_restaurant(request, slug, perm='orders')
    ctx = _shell(request, restaurant, 'orders')
    return render(request, 'cabinet/orders.html', ctx)


@login_required
def orders_feed(request, slug):
    """HTMX-фрагмент: колонки активных заказов (начальная загрузка + резервный опрос)."""
    restaurant = _get_restaurant(request, slug, perm='orders')
    return render(request, 'cabinet/_orders_board.html', _board_context(restaurant, resolve_lang(request)))


@login_required
@require_POST
def order_set_status(request, slug, pk):
    """Сменить статус заказа (вперёд по цепочке / отмена). Realtime разошлётся сам."""
    restaurant = _get_restaurant(request, slug, perm='orders')
    order = get_object_or_404(Order, pk=pk, restaurant=restaurant)
    apply_status_action(order, request.POST.get('action'))
    return render(request, 'cabinet/_orders_board.html', _board_context(restaurant, resolve_lang(request)))


def _board_context(restaurant, lang):
    active = (
        restaurant.orders
        .filter(status__in=Order.FLOW)
        .select_related('table')
        .prefetch_related('items')
    )
    by_status = {st: [] for st in Order.FLOW}
    for order in active:
        by_status[order.status].append(order)

    columns = [
        {'key': st, 'label': translate(lang, f'st_{st}'), 'orders': by_status[st]}
        for st in Order.FLOW
    ]
    # сегодняшние закрытые — просто счётчик
    from django.utils import timezone
    today = timezone.localdate()
    closed_today = restaurant.orders.filter(
        status=Order.Status.CLOSED, updated_at__date=today,
    ).count()
    return {
        'restaurant': restaurant,
        'columns': columns,
        'total_active': active.count(),
        'closed_today': closed_today,
    }
