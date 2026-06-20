import csv
import json
from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import F, Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

# не больше стольких заказов с одного стола за минуту (анти-спам гостевого эндпоинта)
ORDER_RATE_PER_MIN = 8

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

    # стол должен быть «открыт» (визит активен). Закрыт официантом или протух по
    # простою → заказ не принимаем: гость должен заново открыть меню (= новый визит)
    if not table.session_is_open:
        return JsonResponse({'ok': False, 'error': 'table_closed'}, status=409)

    # анти-спам: ограничиваем частоту заказов со стола (qr_token публичен — на столе)
    minute_ago = timezone.now() - timedelta(minutes=1)
    if Order.objects.filter(table=table, created_at__gte=minute_ago).count() >= ORDER_RATE_PER_MIN:
        return JsonResponse({'ok': False, 'error': 'rate_limited'}, status=429)

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
    table.touch_session()  # активность за столом продлевает визит

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
    return render(request, 'cabinet/_orders_board.html',
                  _board_context(restaurant, resolve_lang(request), request.membership))


@login_required
@require_POST
def order_set_status(request, slug, pk):
    """Сменить статус заказа (вперёд по цепочке / отмена). Realtime разошлётся сам."""
    restaurant = _get_restaurant(request, slug, perm='orders')
    order = get_object_or_404(Order, pk=pk, restaurant=restaurant)
    # официант вправе вести только заказы своих (или ничьих) столов
    if not _can_handle_order(order, request.membership):
        return render(request, 'cabinet/_orders_board.html',
                      _board_context(restaurant, resolve_lang(request), request.membership))
    apply_status_action(order, request.POST.get('action'))
    return render(request, 'cabinet/_orders_board.html',
                  _board_context(restaurant, resolve_lang(request), request.membership))


@login_required
@require_POST
def close_table(request, slug, table_pk):
    """Официант закрывает стол после оплаты — новые заказы по нему блокируются."""
    restaurant = _get_restaurant(request, slug, perm='orders')
    table = get_object_or_404(Table, pk=table_pk, restaurant=restaurant)
    # официант вправе закрывать только свои (или ничьи) столы
    waiter_ids = set(table.waiters.values_list('id', flat=True))
    from apps.restaurants.models import Membership
    is_waiter = request.membership and request.membership.role == Membership.Role.WAITER
    if is_waiter and waiter_ids and request.membership.user_id not in waiter_ids:
        pass  # чужой стол — молча игнорируем, просто перерисуем доску
    else:
        table.close_session()
    return render(request, 'cabinet/_orders_board.html',
                  _board_context(restaurant, resolve_lang(request), request.membership))


def _open_tables(restaurant, membership):
    """Столы с активным визитом (для строки «Открытые столы» на доске)."""
    from apps.restaurants.models import Membership, TABLE_SESSION_TTL
    fresh = timezone.now() - TABLE_SESSION_TTL
    qs = restaurant.tables.filter(session_opened_at__gte=fresh)
    if membership and membership.role == Membership.Role.WAITER:
        from django.db.models import Q
        qs = qs.filter(
            Q(waiters=membership.user_id) | Q(waiters__isnull=True)
        ).distinct()
    return qs.order_by('sort_order', 'id')


def _waiter_filtered(qs, membership):
    """Для официанта оставляем заказы его столов + столов без закреплённых
    официантов (общий пул). Остальные роли видят всё."""
    from apps.restaurants.models import Membership
    if membership and membership.role == Membership.Role.WAITER:
        from django.db.models import Q
        qs = qs.filter(
            Q(table__waiters=membership.user_id) | Q(table__waiters__isnull=True)
        ).distinct()
    return qs


def _can_handle_order(order, membership):
    """Может ли сотрудник менять статус конкретного заказа."""
    from apps.restaurants.models import Membership
    if not membership or membership.role != Membership.Role.WAITER:
        return True
    if order.table_id is None:
        return True
    waiter_ids = set(order.table.waiters.values_list('id', flat=True))
    return not waiter_ids or membership.user_id in waiter_ids


@login_required
def orders_history(request, slug):
    """История: закрытые и отменённые заказы с фильтром по периоду + CSV-выгрузка.

    Официант видит историю только своих (или общих) столов — как на доске.
    """
    restaurant = _get_restaurant(request, slug, perm='orders')
    period = request.GET.get('period', '7d')
    if period not in ('today', '7d', '30d', 'all'):
        period = '7d'

    qs = (
        restaurant.orders
        .exclude(status__in=Order.FLOW)  # только закрытые/отменённые
        .select_related('table')
        .prefetch_related('items')
    )
    qs = _waiter_filtered(qs, request.membership)

    today = timezone.localdate()
    if period == 'today':
        qs = qs.filter(created_at__date=today)
    elif period == '30d':
        qs = qs.filter(created_at__date__gte=today - timedelta(days=29))
    elif period == '7d':
        qs = qs.filter(created_at__date__gte=today - timedelta(days=6))
    qs = qs.order_by('-created_at')

    if request.GET.get('export') == 'csv':
        return _history_csv(qs, restaurant, resolve_lang(request))

    # выручка по непогашенным (исключаем отменённые) в выбранном периоде
    revenue = (
        OrderItem.objects
        .filter(order__in=qs.exclude(status=Order.Status.CANCELLED))
        .aggregate(s=Sum(F('price') * F('quantity')))['s'] or 0
    )

    paginator = Paginator(qs, 30)
    page = paginator.get_page(request.GET.get('page'))

    lang = resolve_lang(request)
    ctx = _shell(request, restaurant, 'history')
    ctx.update({
        'orders': page,
        'page_obj': page,
        'period': period,
        'period_tabs': [(k, translate(lang, f'hist_{k}')) for k in ('today', '7d', '30d', 'all')],
        'total_count': paginator.count,
        'total_revenue': f'{revenue:,}'.replace(',', ' '),
    })
    return render(request, 'cabinet/orders_history.html', ctx)


def _history_csv(qs, restaurant, lang):
    resp = HttpResponse(content_type='text/csv; charset=utf-8')
    resp['Content-Disposition'] = f'attachment; filename="orders-{restaurant.slug}.csv"'
    resp.write('﻿')  # BOM, чтобы Excel понял UTF-8
    writer = csv.writer(resp)
    writer.writerow(['#', 'Дата', 'Стол', 'Статус', 'Позиций', 'Сумма (сум)'])
    for o in qs:
        writer.writerow([
            o.pk,
            timezone.localtime(o.created_at).strftime('%Y-%m-%d %H:%M'),
            o.table.name if o.table else '—',
            translate(lang, f'st_{o.status}'),
            sum(i.quantity for i in o.items.all()),
            o.total,
        ])
    return resp


def _board_context(restaurant, lang, membership=None):
    active = _waiter_filtered(
        restaurant.orders
        .filter(status__in=Order.FLOW)
        .select_related('table')
        .prefetch_related('items'),
        membership,
    )
    by_status = {st: [] for st in Order.FLOW}
    total_active = 0
    for order in active:
        by_status[order.status].append(order)
        total_active += 1

    columns = [
        {'key': st, 'label': translate(lang, f'st_{st}'), 'orders': by_status[st]}
        for st in Order.FLOW
    ]
    # сегодняшние закрытые — просто счётчик (с тем же фильтром по столам)
    from django.utils import timezone
    today = timezone.localdate()
    closed_today = _waiter_filtered(
        restaurant.orders.filter(status=Order.Status.CLOSED, updated_at__date=today),
        membership,
    ).count()
    return {
        'restaurant': restaurant,
        'columns': columns,
        'total_active': total_active,
        'closed_today': closed_today,
        'open_tables': _open_tables(restaurant, membership),
    }
