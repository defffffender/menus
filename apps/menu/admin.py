from django.contrib import admin
from unfold.admin import ModelAdmin as UnfoldModelAdmin
from unfold.admin import TabularInline as UnfoldTabularInline

from .models import Category, Dish, DishVariant


class DishVariantInline(UnfoldTabularInline):
    model = DishVariant
    extra = 1


@admin.register(Category)
class CategoryAdmin(UnfoldModelAdmin):
    list_display = ('name_ru', 'restaurant', 'sort_order', 'is_active')
    list_filter = ('is_active', 'restaurant')
    search_fields = ('name_ru', 'name_uz', 'name_en', 'restaurant__name')
    autocomplete_fields = ('restaurant',)


@admin.register(Dish)
class DishAdmin(UnfoldModelAdmin):
    list_display = ('name_ru', 'category', 'is_available', 'sort_order')
    list_filter = ('is_available', 'spiciness', 'category__restaurant')
    search_fields = ('name_ru', 'name_uz', 'name_en')
    autocomplete_fields = ('category',)
    inlines = (DishVariantInline,)


@admin.register(DishVariant)
class DishVariantAdmin(UnfoldModelAdmin):
    list_display = ('dish', 'name_ru', 'price', 'sort_order')
    search_fields = ('dish__name_ru', 'name_ru')
    autocomplete_fields = ('dish',)
