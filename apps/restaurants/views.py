import io
import json
import re

import qrcode
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, F, Sum
from django.db.models.functions import TruncDate
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST

from apps.core.images import MAX_UPLOAD_MB, downscale_field
from apps.core.translations import resolve_lang
from apps.core.translations import t as translate
from apps.core.translations import tr

from .access import (
    assignable_roles,
    can,
    can_manage,
    membership_for,
    owns_any_venue,
    perms_of,
)
from .forms import RestaurantForm, TableForm
from .middleware import SubscriptionBlocked
from .models import (
    FONT_PAIRS,
    RADIUS_PX,
    Membership,
    MenuTheme,
    Restaurant,
    Table,
    TableZone,
)


def _get_restaurant(request, slug, perm=None):
    """Заведение текущего пользователя. `perm` — требуемая зона доступа (RBAC).

    Прячем и отсутствие доступа, и нехватку прав за 404 (не светим существование).
    Найденную роль кладём в `request.membership` для шелла и шаблонов.
    """
    restaurant = get_object_or_404(Restaurant.objects.select_related('owner'), slug=slug)
    membership = membership_for(request.user, restaurant)
    if membership is None:
        raise Http404
    if perm is not None and not can(membership, perm):
        raise Http404
    # подписка владельца истекла/приостановлена → кабинет недоступен
    if restaurant.subscription_blocked:
        raise SubscriptionBlocked(restaurant)
    request.membership = membership
    return restaurant


def _shell(request, restaurant, active):
    """Общий контекст для шелла кабинета (сайдбар, переключатель заведений)."""
    membership = getattr(request, 'membership', None) or membership_for(request.user, restaurant)
    role_label = translate(resolve_lang(request), f'role_{membership.role}') if membership else ''
    venues = list(
        request.user.memberships
        .select_related('restaurant')
        .filter(is_active=True)
    )
    has_other = any(v.restaurant_id != restaurant.id for v in venues)
    perms = perms_of(membership)
    ctx = {
        'restaurant': restaurant,
        'active': active,
        'membership': membership,
        'role_label': role_label,
        'perms': perms,
        # самостоятельно заводить заведения владельцы больше не могут — только агенты
        'can_create_venue': False,
        # переключатель показываем только если есть куда переключиться
        'can_switch_venue': has_other,
        'venues': venues,
    }
    # счётчики для бейджей в сайдбаре (меню — блюд, заказы — активных)
    if 'menu' in perms:
        from apps.menu.models import Dish
        ctx['nav_menu_count'] = Dish.objects.filter(category__restaurant=restaurant).count()
    if 'orders' in perms:
        from apps.orders.models import Order
        ctx['nav_orders_count'] = restaurant.orders.filter(status__in=Order.FLOW).count()
    return ctx


@login_required
def cabinet(request):
    """Список заведений пользователя. Если оно одно — сразу в дашборд."""
    # агент управляет заведениями из своего агентского кабинета
    if request.user.is_agent_user:
        return redirect('accounts:agent_dashboard')
    memberships = (
        request.user.memberships
        .select_related('restaurant')
        .filter(is_active=True)
    )
    if memberships.count() == 1:
        return redirect('restaurants:dashboard', slug=memberships[0].restaurant.slug)
    return render(request, 'restaurants/cabinet.html', {
        'memberships': memberships,
        'can_create_venue': False,
    })


@login_required
def venue_create(request):
    """Создание заведений доступно только агентам — через агентский кабинет.
    Владельцы заведения самостоятельно их не заводят."""
    if request.user.is_agent_user:
        return redirect('accounts:agent_register_venue')
    raise Http404


@login_required
def dashboard(request, slug):
    restaurant = _get_restaurant(request, slug)
    from apps.menu.models import Dish
    from apps.orders.models import Order
    ctx = _shell(request, restaurant, 'dashboard')
    ctx['tables_count'] = restaurant.tables.count()
    ctx['dishes_count'] = Dish.objects.filter(category__restaurant=restaurant).count()
    ctx['active_orders'] = restaurant.orders.filter(status__in=Order.FLOW).count()
    return render(request, 'cabinet/dashboard.html', ctx)


def _restaurant_waiters(restaurant):
    """Действующие официанты заведения (для закрепления за столами)."""
    return [
        {'id': m.user_id, 'label': m.user.full_name or m.user.phone}
        for m in (
            restaurant.memberships
            .filter(role=Membership.Role.WAITER, is_active=True)
            .select_related('user')
            .order_by('user__full_name', 'user__phone')
        )
    ]


def _zone_groups(restaurant):
    """Столы, сгруппированные по зонам. Каждый стол с набором id официантов.
    Зоны идут по порядку, в конце — группа «без зоны» (если такие есть)."""
    tables = list(
        restaurant.tables.select_related('zone').prefetch_related('waiters')
    )
    for tb in tables:
        tb.waiter_ids = {u.id for u in tb.waiters.all()}
    zones = list(restaurant.zones.annotate(n_tables=Count('tables')))
    groups = []
    for z in zones:
        zt = [t for t in tables if t.zone_id == z.id]
        groups.append({'zone': z, 'tables': zt})
    unzoned = [t for t in tables if t.zone_id is None]
    if unzoned:
        groups.append({'zone': None, 'tables': unzoned})
    return groups, zones


def _apply_zone(table, restaurant, raw_zone):
    """Проставить столу зону из POST (или снять), проверив принадлежность заведению."""
    if raw_zone and str(raw_zone).isdigit():
        table.zone = restaurant.zones.filter(pk=int(raw_zone)).first()
    else:
        table.zone = None


@login_required
def tables(request, slug):
    restaurant = _get_restaurant(request, slug, perm='tables')
    if request.method == 'POST':
        form = TableForm(request.POST)
        if form.is_valid():
            table = form.save(commit=False)
            table.restaurant = restaurant
            _apply_zone(table, restaurant, request.POST.get('zone'))
            table.save()
            return redirect('restaurants:tables', slug=slug)
    else:
        form = TableForm()
    groups, zones = _zone_groups(restaurant)
    ctx = _shell(request, restaurant, 'tables')
    ctx['groups'] = groups
    ctx['zones'] = zones
    ctx['has_tables'] = any(g['tables'] for g in groups)
    ctx['waiters'] = _restaurant_waiters(restaurant)
    ctx['form'] = form
    return render(request, 'cabinet/tables.html', ctx)


def _parse_order_ids(request):
    try:
        data = json.loads(request.body or '{}')
        return [int(x) for x in data.get('order', [])]
    except (ValueError, TypeError):
        return []


@login_required
@require_POST
def zone_reorder(request, slug):
    """Сохранить новый порядок зон (drag-and-drop)."""
    restaurant = _get_restaurant(request, slug, perm='tables')
    ids = _parse_order_ids(request)
    zones = {z.pk: z for z in restaurant.zones.filter(pk__in=ids)}
    changed = []
    for i, pk in enumerate(ids):
        z = zones.get(pk)
        if z is not None and z.sort_order != i:
            z.sort_order = i
            changed.append(z)
    if changed:
        TableZone.objects.bulk_update(changed, ['sort_order'])
    return JsonResponse({'ok': True})


@login_required
@require_POST
def table_reorder(request, slug):
    """Сохранить новый порядок столов внутри зоны (drag-and-drop)."""
    restaurant = _get_restaurant(request, slug, perm='tables')
    ids = _parse_order_ids(request)
    tables = {t.pk: t for t in restaurant.tables.filter(pk__in=ids)}
    changed = []
    for i, pk in enumerate(ids):
        t = tables.get(pk)
        if t is not None and t.sort_order != i:
            t.sort_order = i
            changed.append(t)
    if changed:
        Table.objects.bulk_update(changed, ['sort_order'])
    return JsonResponse({'ok': True})


@login_required
def zone_add(request, slug):
    restaurant = _get_restaurant(request, slug, perm='tables')
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()[:80]
        if name:
            last = restaurant.zones.order_by('-sort_order').first()
            order = (last.sort_order + 1) if last else 0
            TableZone.objects.create(restaurant=restaurant, name=name, sort_order=order)
            messages.success(request, tr(request, 'zone_created'))
    return redirect('restaurants:tables', slug=slug)


@login_required
def zone_edit(request, slug, pk):
    restaurant = _get_restaurant(request, slug, perm='tables')
    zone = get_object_or_404(TableZone, pk=pk, restaurant=restaurant)
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()[:80]
        if name:
            zone.name = name
            zone.save(update_fields=['name'])
            messages.success(request, tr(request, 'set_saved'))
    return redirect('restaurants:tables', slug=slug)


@login_required
@require_POST
def zone_delete(request, slug, pk):
    """Удалить зону. Столы зоны остаются — становятся «без зоны»."""
    restaurant = _get_restaurant(request, slug, perm='tables')
    zone = get_object_or_404(TableZone, pk=pk, restaurant=restaurant)
    zone.delete()
    messages.success(request, tr(request, 'zone_deleted'))
    return redirect('restaurants:tables', slug=slug)


@login_required
@require_POST
def table_waiters(request, slug, pk):
    """Закрепить официантов за столом (мультивыбор). Принимаем только
    действующих официантов этого заведения."""
    restaurant = _get_restaurant(request, slug, perm='tables')
    table = get_object_or_404(Table, pk=pk, restaurant=restaurant)
    valid_ids = {w['id'] for w in _restaurant_waiters(restaurant)}
    chosen = {int(x) for x in request.POST.getlist('waiters') if x.isdigit()}
    table.waiters.set(valid_ids & chosen)
    messages.success(request, tr(request, 'tables_waiters_saved'))
    return redirect('restaurants:tables', slug=slug)


@login_required
def table_edit(request, slug, pk):
    restaurant = _get_restaurant(request, slug, perm='tables')
    table = get_object_or_404(Table, pk=pk, restaurant=restaurant)
    if request.method == 'POST':
        form = TableForm(request.POST, instance=table)
        if form.is_valid():
            table = form.save(commit=False)
            _apply_zone(table, restaurant, request.POST.get('zone'))
            table.save()
            return redirect('restaurants:tables', slug=slug)
    else:
        form = TableForm(instance=table)
    groups, zones = _zone_groups(restaurant)
    ctx = _shell(request, restaurant, 'tables')
    ctx['groups'] = groups
    ctx['zones'] = zones
    ctx['has_tables'] = any(g['tables'] for g in groups)
    ctx['waiters'] = _restaurant_waiters(restaurant)
    ctx['form'] = form
    ctx['edit_table'] = table
    return render(request, 'cabinet/tables.html', ctx)


@login_required
def table_delete(request, slug, pk):
    restaurant = _get_restaurant(request, slug, perm='tables')
    table = get_object_or_404(Table, pk=pk, restaurant=restaurant)
    if request.method == 'POST':
        table.delete()
    return redirect('restaurants:tables', slug=slug)


@login_required
def table_qr_png(request, slug, pk):
    restaurant = _get_restaurant(request, slug, perm='tables')
    table = get_object_or_404(Table, pk=pk, restaurant=restaurant)
    url = request.build_absolute_uri(
        reverse('restaurants:guest_menu', args=[table.qr_token])
    )
    img = qrcode.make(url, box_size=10, border=2)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    return HttpResponse(buf.getvalue(), content_type='image/png')


@login_required
def qr_sheet(request, slug):
    restaurant = _get_restaurant(request, slug, perm='tables')
    groups, _ = _zone_groups(restaurant)
    ctx = _shell(request, restaurant, 'qr')
    ctx['groups'] = groups
    ctx['has_tables'] = any(g['tables'] for g in groups)
    return render(request, 'cabinet/qr_sheet.html', ctx)


# --- сотрудники --------------------------------------------------------------

def _staff_admin_venues(user):
    """Заведения, куда этот пользователь вправе привязывать сотрудников
    в любое (владелец/директор). Для них показываем выбор заведения."""
    Role = Membership.Role
    return list(
        Membership.objects
        .filter(user=user, is_active=True, role__in=[Role.OWNER, Role.DIRECTOR])
        .select_related('restaurant')
    )


@login_required
def staff(request, slug):
    """Список сотрудников + приглашение по телефону (доступ — зона staff).

    Владелец/директор может сразу привязать сотрудника к любому своему
    заведению, не переключаясь в его кабинет.
    """
    from apps.accounts.models import User, is_valid_uz_phone, normalize_phone

    restaurant = _get_restaurant(request, slug, perm='staff')
    actor = request.membership
    allowed = assignable_roles(actor)
    allowed_values = {r.value for r in allowed}

    # заведения, между которыми можно выбирать при приглашении
    admin_venues = _staff_admin_venues(request.user)
    show_venue_picker = (
        actor.role in (Membership.Role.OWNER, Membership.Role.DIRECTOR)
        and len(admin_venues) > 1
    )

    if request.method == 'POST':
        raw_phone = request.POST.get('phone', '')
        phone = normalize_phone(raw_phone)
        full_name = request.POST.get('full_name', '').strip()
        role = request.POST.get('role', '')

        # к каким заведениям привязываем. Мультивыбор — только для владельца/
        # директора с несколькими заведениями; иначе всегда текущее.
        if show_venue_picker:
            target_slugs = request.POST.getlist('venues') or []
        else:
            target_slugs = [slug]

        # резолвим цели и проверяем права на каждое
        targets = []  # (restaurant, role) валидные
        bad_perm = False
        bad_role = False
        for ts in target_slugs:
            t = Restaurant.objects.filter(slug=ts).first()
            tm = membership_for(request.user, t) if t else None
            if tm is None or tm.role not in (Membership.Role.OWNER, Membership.Role.DIRECTOR):
                bad_perm = True
                continue
            if role not in {r.value for r in assignable_roles(tm)}:
                bad_role = True
                continue
            targets.append(t)

        if not is_valid_uz_phone(raw_phone):
            messages.error(request, tr(request, 'err_phone_uz'))
        elif not target_slugs:
            messages.error(request, tr(request, 'staff_err_no_venue'))
        elif bad_perm:
            messages.error(request, tr(request, 'staff_err_venue'))
        elif bad_role or not targets:
            messages.error(request, tr(request, 'staff_err_role'))
        else:
            user, created = User.objects.get_or_create(
                phone=phone, defaults={'full_name': full_name},
            )
            if created:
                user.set_unusable_password()
                user.save()
            elif full_name and not user.full_name:
                user.full_name = full_name
                user.save(update_fields=['full_name'])
            added = 0
            for t in targets:
                _, m_created = Membership.objects.get_or_create(
                    user=user, restaurant=t, defaults={'role': role},
                )
                added += 1 if m_created else 0
            if added:
                msg = tr(request, 'staff_added')
                if len(targets) > 1:
                    msg = f"{tr(request, 'staff_added_n')}: {added}"
                messages.success(request, msg)
            else:
                messages.error(request, tr(request, 'staff_err_exists'))
        return redirect('restaurants:staff', slug=slug)

    lang = resolve_lang(request)
    members = (
        restaurant.memberships
        .select_related('user')
        .order_by('-is_active', 'role', 'created_at')
    )
    rows = [
        {
            'm': m,
            'role_label': translate(lang, f'role_{m.role}'),
            'can_manage': can_manage(actor, m),
            'is_self': m.pk == actor.pk,
        }
        for m in members
    ]
    ctx = _shell(request, restaurant, 'staff')
    ctx['rows'] = rows
    ctx['assignable'] = [(r.value, translate(lang, f'role_{r.value}')) for r in allowed]
    ctx['show_venue_picker'] = show_venue_picker
    ctx['venue_choices'] = [m.restaurant for m in admin_venues] if show_venue_picker else []
    return render(request, 'cabinet/staff.html', ctx)


@login_required
def staff_role(request, slug, pk):
    """Сменить роль сотрудника (только на роль из допустимых актору)."""
    restaurant = _get_restaurant(request, slug, perm='staff')
    target = get_object_or_404(Membership, pk=pk, restaurant=restaurant)
    if request.method == 'POST' and can_manage(request.membership, target):
        role = request.POST.get('role', '')
        if role in {r.value for r in assignable_roles(request.membership)}:
            target.role = role
            target.save(update_fields=['role'])
    return redirect('restaurants:staff', slug=slug)


@login_required
def staff_remove(request, slug, pk):
    """Убрать сотрудника из заведения (деактивировать membership)."""
    restaurant = _get_restaurant(request, slug, perm='staff')
    target = get_object_or_404(Membership, pk=pk, restaurant=restaurant)
    if request.method == 'POST' and can_manage(request.membership, target):
        target.delete()
    return redirect('restaurants:staff', slug=slug)


# --- аналитика ---------------------------------------------------------------

@login_required
def analytics(request, slug):
    """Сводка по заказам: сегодня, неделя, топ блюд. Оплату не считаем —
    «выручка» = сумма незаотменённых заказов (что заказали)."""
    from apps.orders.models import Order, OrderItem

    restaurant = _get_restaurant(request, slug, perm='analytics')
    today = timezone.localdate()
    week_start = today - timezone.timedelta(days=6)

    def revenue(qs):
        return qs.aggregate(s=Sum(F('price') * F('quantity')))['s'] or 0

    # сегодня
    today_orders = restaurant.orders.filter(created_at__date=today).exclude(status=Order.Status.CANCELLED)
    today_count = today_orders.count()
    today_rev = revenue(OrderItem.objects.filter(order__in=today_orders))
    avg_check = today_rev // today_count if today_count else 0

    # неделя (7 дней)
    week_orders = restaurant.orders.filter(created_at__date__gte=week_start).exclude(status=Order.Status.CANCELLED)
    week_count = week_orders.count()
    week_rev = revenue(OrderItem.objects.filter(order__in=week_orders))

    # топ-5 блюд за неделю
    top = list(
        OrderItem.objects.filter(order__in=week_orders)
        .values('name')
        .annotate(qty=Sum('quantity'), rev=Sum(F('price') * F('quantity')))
        .order_by('-qty')[:5]
    )
    for t in top:
        t['rev_display'] = _money(t['rev'])

    # дневная динамика за 7 дней — одним сгруппированным запросом (было ~14)
    tz = timezone.get_current_timezone()
    by_day = {
        row['d']: row
        for row in (
            week_orders
            .annotate(d=TruncDate('created_at', tzinfo=tz))
            .values('d')
            .annotate(
                n=Count('id', distinct=True),
                rev=Sum(F('items__price') * F('items__quantity')),
            )
        )
    }
    days = [week_start + timezone.timedelta(days=i) for i in range(7)]
    chart_labels, chart_orders, chart_revenue = [], [], []
    for d in days:
        row = by_day.get(d)
        chart_labels.append(d.strftime('%d.%m'))
        chart_orders.append(row['n'] if row else 0)
        chart_revenue.append(int(row['rev'] or 0) if row else 0)

    chart = {
        'labels': chart_labels,
        'orders': chart_orders,
        'revenue': chart_revenue,
        'top_labels': [t['name'] for t in top],
        'top_qty': [t['qty'] for t in top],
        'i18n': {
            'orders': translate(resolve_lang(request), 'an_orders'),
            'revenue': translate(resolve_lang(request), 'an_revenue'),
            'qty': translate(resolve_lang(request), 'an_qty'),
        },
    }

    ctx = _shell(request, restaurant, 'analytics')
    ctx.update({
        'active_now': restaurant.orders.filter(status__in=Order.FLOW).count(),
        'today_count': today_count,
        'today_rev': _money(today_rev),
        'avg_check': _money(avg_check),
        'week_count': week_count,
        'week_rev': _money(week_rev),
        'top': top,
        'chart': chart,
        'has_chart_data': bool(week_count),
    })
    return render(request, 'cabinet/analytics.html', ctx)


# --- настройки заведения -----------------------------------------------------

@login_required
def settings_view(request, slug):
    """Профиль заведения: название, тип, город, телефон, лого, описания (3 языка)."""
    restaurant = _get_restaurant(request, slug, perm='settings')
    if request.method == 'POST':
        form = RestaurantForm(request.POST, request.FILES, instance=restaurant)
        if form.is_valid():
            form.save()
            messages.success(request, tr(request, 'set_saved'))
            return redirect('restaurants:settings', slug=slug)
    else:
        form = RestaurantForm(instance=restaurant)
    from apps.menu.models import Dish
    owner = restaurant.owner
    plan_label_key = {'start': 'l_plan_start', 'business': 'l_plan_pro', 'network': 'l_plan_net'}.get(owner.plan, 'l_plan_start')
    ctx = _shell(request, restaurant, 'settings')
    ctx['form'] = form
    ctx['plan_label'] = translate(resolve_lang(request), plan_label_key)
    ctx['venue_limit'] = owner.venue_limit
    ctx['venues_used'] = owner.venues_used
    ctx['dish_limit'] = owner.dish_limit
    ctx['dishes_used'] = Dish.objects.filter(category__restaurant=restaurant).count()
    return render(request, 'cabinet/settings.html', ctx)


def _money(value):
    """Целое в сумах → «38 000» (разделитель — неразрывный пробел)."""
    return f'{value:,}'.replace(',', ' ')


def _build_menu(restaurant, lang):
    """Меню заведения для публичного показа: категории → блюда → варианты."""
    categories = (
        restaurant.categories
        .filter(is_active=True)
        .prefetch_related('dishes__variants')
    )
    menu = []
    for cat in categories:
        dishes = []
        for d in cat.dishes.all():
            variants = [
                {'id': v.pk, 'name': v.name(lang), 'price': v.price, 'price_display': _money(v.price)}
                for v in d.variants.all()
            ]
            if not variants:
                continue
            dishes.append({
                'id': d.pk,
                'name': d.name(lang),
                'description': getattr(d, f'description_{lang}', '') or d.description_ru,
                'photo': d.photo,
                'weight': d.weight,
                'available': d.is_available,
                'variants': variants,
                'multi': len(variants) > 1,
            })
        if dishes:
            menu.append({'name': cat.name(lang), 'dishes': dishes})
    return menu


@ensure_csrf_cookie
def guest_menu(request, qr_token):
    """Публичное меню стола: гость смотрит и собирает корзину (без регистрации)."""
    table = get_object_or_404(
        Table.objects.select_related('restaurant', 'restaurant__owner'),
        qr_token=qr_token, is_active=True,
    )
    restaurant = table.restaurant
    if restaurant.subscription_blocked:
        return render(request, 'public/menu_unavailable.html', {'restaurant': restaurant}, status=402)
    lang = resolve_lang(request)
    # просмотр меню = «сканирование»: открываем визит, если стол сейчас закрыт.
    # НО если официант только что закрыл стол (идёт кулдаун) — не переоткрываем:
    # это защита от «заказа из дома», когда ушедший гость перезагружает страницу.
    # Для новой компании официант открывает стол вручную кнопкой на доске.
    if not table.session_is_open and not table.reopen_blocked:
        table.open_session()
    return render(request, 'public/menu.html', {
        'table': table,
        'restaurant': restaurant,
        'menu': _build_menu(restaurant, lang),
        'theme': MenuTheme.for_restaurant(restaurant),
    })


# --- дизайн меню -------------------------------------------------------------

_HEX = re.compile(r'^#[0-9A-Fa-f]{6}$')


def _clean_hex(value, fallback):
    value = (value or '').strip()
    return value if _HEX.match(value) else fallback


@login_required
def menu_design(request, slug):
    """Конструктор темы гостевого меню: цвета, шрифт, карточки, логотип/шапка."""
    restaurant = _get_restaurant(request, slug, perm='design')
    theme, _created = MenuTheme.objects.get_or_create(restaurant=restaurant)

    if request.method == 'POST':
        theme.accent = _clean_hex(request.POST.get('accent'), theme.accent)
        theme.bg = _clean_hex(request.POST.get('bg'), theme.bg)
        theme.text = _clean_hex(request.POST.get('text'), theme.text)
        theme.card_bg = _clean_hex(request.POST.get('card_bg'), theme.card_bg)
        if request.POST.get('font') in FONT_PAIRS:
            theme.font = request.POST['font']
        if request.POST.get('card_style') in MenuTheme.Card.values:
            theme.card_style = request.POST['card_style']
        if request.POST.get('radius') in MenuTheme.Radius.values:
            theme.radius = request.POST['radius']
        if request.POST.get('header_layout') in MenuTheme.Header.values:
            theme.header_layout = request.POST['header_layout']
        theme.show_desc = bool(request.POST.get('show_desc'))
        theme.show_logo = bool(request.POST.get('show_logo'))
        if request.POST.get('cover_clear') and theme.cover:
            theme.cover.delete(save=False)
            theme.cover = None
        cover = request.FILES.get('cover')
        if cover and cover.size > MAX_UPLOAD_MB * 1024 * 1024:
            messages.error(request, tr(request, 'design_cover_big'))
            return redirect('restaurants:menu_design', slug=slug)
        if cover:
            theme.cover = cover
        theme.save()
        if cover:
            downscale_field(theme.cover, max_px=1600)
            theme.save(update_fields=['cover'])
        messages.success(request, tr(request, 'design_saved'))
        return redirect('restaurants:menu_design', slug=slug)

    ctx = _shell(request, restaurant, 'design')
    ctx['theme'] = theme
    ctx['fonts'] = [(k, v['label'], v['display'], v['body'], v['google']) for k, v in FONT_PAIRS.items()]
    ctx['radius_map'] = RADIUS_PX
    return render(request, 'cabinet/menu_design.html', ctx)


@login_required
@xframe_options_sameorigin
def menu_design_preview(request, slug):
    """Контент iframe-превью в редакторе: настоящее меню заведения с текущей темой.

    `xframe_options_sameorigin` снимает дефолтный X-Frame-Options: DENY —
    иначе браузер откажется встраивать превью в <iframe> редактора.
    """
    restaurant = _get_restaurant(request, slug, perm='design')
    lang = resolve_lang(request)
    return render(request, 'public/menu.html', {
        'table': None,
        'restaurant': restaurant,
        'menu': _build_menu(restaurant, lang),
        'theme': MenuTheme.for_restaurant(restaurant),
        'preview': True,
    })
