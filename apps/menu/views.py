from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from apps.restaurants.views import _get_restaurant, _shell

from .forms import CategoryForm, DishForm
from .models import Category, Dish, DishVariant


@login_required
def menu(request, slug):
    """Список меню: категории с вложенными блюдами."""
    restaurant = _get_restaurant(request, slug, perm='menu')
    ctx = _shell(request, restaurant, 'menu')
    ctx['categories'] = (
        restaurant.categories
        .prefetch_related('dishes__variants')
        .all()
    )
    ctx['dishes_count'] = Dish.objects.filter(category__restaurant=restaurant).count()
    return render(request, 'cabinet/menu.html', ctx)


# --- категории ---------------------------------------------------------------

@login_required
def category_add(request, slug):
    restaurant = _get_restaurant(request, slug, perm='menu')
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.restaurant = restaurant
            category.save()
            messages.success(request, 'OK')
    return redirect('menu:menu', slug=slug)


@login_required
def category_edit(request, slug, pk):
    restaurant = _get_restaurant(request, slug, perm='menu')
    category = get_object_or_404(Category, pk=pk, restaurant=restaurant)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
    return redirect('menu:menu', slug=slug)


@login_required
def category_delete(request, slug, pk):
    restaurant = _get_restaurant(request, slug, perm='menu')
    category = get_object_or_404(Category, pk=pk, restaurant=restaurant)
    if request.method == 'POST':
        category.delete()
    return redirect('menu:menu', slug=slug)


# --- блюда -------------------------------------------------------------------

def _save_variants(request, dish):
    """Пересобирает варианты блюда из параллельных списков формы.

    Каждая строка: v_id, v_name_ru/uz/en, v_price. Пустые строки (без цены)
    игнорируются; существующие варианты, которых нет в форме, удаляются.
    """
    ids = request.POST.getlist('v_id')
    names_ru = request.POST.getlist('v_name_ru')
    names_uz = request.POST.getlist('v_name_uz')
    names_en = request.POST.getlist('v_name_en')
    prices = request.POST.getlist('v_price')

    kept_ids = []
    for i, raw_price in enumerate(prices):
        raw_price = (raw_price or '').strip()
        if not raw_price:
            continue
        try:
            price = int(raw_price)
        except ValueError:
            continue
        if price < 0:
            continue
        vid = ids[i] if i < len(ids) else ''
        data = {
            'name_ru': names_ru[i].strip() if i < len(names_ru) else '',
            'name_uz': names_uz[i].strip() if i < len(names_uz) else '',
            'name_en': names_en[i].strip() if i < len(names_en) else '',
            'price': price,
            'sort_order': i,
        }
        if vid:
            DishVariant.objects.filter(pk=vid, dish=dish).update(**data)
            kept_ids.append(int(vid))
        else:
            variant = DishVariant.objects.create(dish=dish, **data)
            kept_ids.append(variant.pk)

    # удалить варианты, убранные из формы
    dish.variants.exclude(pk__in=kept_ids).delete()


def _has_price(request):
    return any((p or '').strip() for p in request.POST.getlist('v_price'))


def _dish_limit_reached(restaurant):
    """Достигнут ли лимит блюд тарифа владельца заведения."""
    limit = restaurant.owner.dish_limit
    if limit is None:
        return False
    return Dish.objects.filter(category__restaurant=restaurant).count() >= limit


@login_required
def dish_add(request, slug):
    from apps.core.translations import tr
    restaurant = _get_restaurant(request, slug, perm='menu')
    if request.method == 'POST':
        if _dish_limit_reached(restaurant):
            messages.error(request, tr(request, 'plan_limit_dishes'))
            return redirect('menu:menu', slug=slug)
        form = DishForm(request.POST, request.FILES, restaurant=restaurant)
        if form.is_valid() and _has_price(request):
            dish = form.save()
            _save_variants(request, dish)
            messages.success(request, 'Блюдо добавлено')
            return redirect('menu:menu', slug=slug)
        if not _has_price(request):
            messages.error(request, 'Укажите хотя бы одну цену')
    else:
        if _dish_limit_reached(restaurant):
            messages.error(request, tr(request, 'plan_limit_dishes'))
            return redirect('menu:menu', slug=slug)
        form = DishForm(restaurant=restaurant)
    ctx = _shell(request, restaurant, 'menu')
    ctx['form'] = form
    ctx['categories'] = restaurant.categories.all()
    ctx['variants'] = []
    return render(request, 'cabinet/dish_form.html', ctx)


@login_required
def dish_edit(request, slug, pk):
    restaurant = _get_restaurant(request, slug, perm='menu')
    dish = get_object_or_404(Dish, pk=pk, category__restaurant=restaurant)
    if request.method == 'POST':
        form = DishForm(request.POST, request.FILES, instance=dish, restaurant=restaurant)
        if form.is_valid() and _has_price(request):
            dish = form.save()
            _save_variants(request, dish)
            messages.success(request, 'Сохранено')
            return redirect('menu:menu', slug=slug)
        if not _has_price(request):
            messages.error(request, 'Укажите хотя бы одну цену')
    else:
        form = DishForm(instance=dish, restaurant=restaurant)
    ctx = _shell(request, restaurant, 'menu')
    ctx['form'] = form
    ctx['dish'] = dish
    ctx['categories'] = restaurant.categories.all()
    ctx['variants'] = dish.variants.all()
    return render(request, 'cabinet/dish_form.html', ctx)


@login_required
def dish_delete(request, slug, pk):
    restaurant = _get_restaurant(request, slug, perm='menu')
    dish = get_object_or_404(Dish, pk=pk, category__restaurant=restaurant)
    if request.method == 'POST':
        dish.delete()
    return redirect('menu:menu', slug=slug)


@login_required
def dish_toggle(request, slug, pk):
    """Быстрый стоп-лист: переключить наличие блюда."""
    restaurant = _get_restaurant(request, slug, perm='menu')
    dish = get_object_or_404(Dish, pk=pk, category__restaurant=restaurant)
    if request.method == 'POST':
        dish.is_available = not dish.is_available
        dish.save(update_fields=['is_available'])
    return redirect('menu:menu', slug=slug)
