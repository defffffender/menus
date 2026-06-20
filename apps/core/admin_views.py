"""Данные для платформенного дашборда в /admin (для владельца сервиса).

Считается поверх ВСЕХ заведений: регистрации, заказы и выручка по дням,
распределение пользователей по тарифам, сводные счётчики.
"""
from datetime import timedelta

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, F, Sum
from django.db.models.functions import TruncDate
from django.http import JsonResponse
from django.utils import timezone

from apps.accounts.models import User
from apps.orders.models import Order, OrderItem
from apps.restaurants.models import Restaurant

DAYS = 14


@staff_member_required
def admin_dashboard_data(request):
    tz = timezone.get_current_timezone()
    today = timezone.localdate()
    days = [today - timedelta(days=i) for i in range(DAYS - 1, -1, -1)]
    labels = [d.strftime('%d.%m') for d in days]
    idx = {d: i for i, d in enumerate(days)}
    start = days[0]

    def by_day(queryset, day_field, value=None):
        """Свернуть queryset по календарным дням в список длины DAYS."""
        out = [0] * DAYS
        grouped = (
            queryset
            .annotate(_day=TruncDate(day_field, tzinfo=tz))
            .values('_day')
            .annotate(_v=value if value is not None else Count('id'))
        )
        for row in grouped:
            if row['_day'] in idx:
                out[idx[row['_day']]] = int(row['_v'] or 0)
        return out

    registrations = by_day(
        Restaurant.objects.filter(created_at__date__gte=start), 'created_at',
    )
    live_orders = Order.objects.filter(created_at__date__gte=start).exclude(status=Order.Status.CANCELLED)
    orders = by_day(live_orders, 'created_at')
    revenue = by_day(
        OrderItem.objects.filter(order__in=live_orders), 'order__created_at',
        value=Sum(F('price') * F('quantity')),
    )

    plan_labels = dict(User._meta.get_field('plan').choices)
    plans = [
        {'label': str(plan_labels.get(r['plan'], r['plan'])), 'n': r['n']}
        for r in User.objects.values('plan').annotate(n=Count('id')).order_by('-n')
    ]

    cards = {
        'restaurants': Restaurant.objects.count(),
        'users': User.objects.count(),
        'orders_today': orders[-1],
        'revenue_14d': sum(revenue),
    }

    return JsonResponse({
        'labels': labels,
        'registrations': registrations,
        'orders': orders,
        'revenue': revenue,
        'plans': plans,
        'cards': cards,
    })
