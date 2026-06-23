from django.contrib import admin
from unfold.admin import ModelAdmin as UnfoldModelAdmin
from unfold.admin import TabularInline as UnfoldTabularInline

from .models import Membership, MenuTheme, Restaurant, Table, TableZone


class MembershipInline(UnfoldTabularInline):
    model = Membership
    extra = 1
    autocomplete_fields = ('user',)


@admin.register(Restaurant)
class RestaurantAdmin(UnfoldModelAdmin):
    list_display = ('name', 'type', 'city', 'owner', 'is_active', 'created_at')
    list_filter = ('type', 'is_active', 'city')
    search_fields = ('name', 'slug', 'phone')
    prepopulated_fields = {'slug': ('name',)}
    autocomplete_fields = ('owner',)
    inlines = (MembershipInline,)


@admin.register(Membership)
class MembershipAdmin(UnfoldModelAdmin):
    list_display = ('user', 'restaurant', 'role', 'is_active', 'created_at')
    list_filter = ('role', 'is_active')
    search_fields = ('user__phone', 'user__full_name', 'restaurant__name')
    autocomplete_fields = ('user', 'restaurant')


@admin.register(MenuTheme)
class MenuThemeAdmin(UnfoldModelAdmin):
    list_display = ('restaurant', 'font', 'card_style', 'updated_at')
    search_fields = ('restaurant__name',)
    autocomplete_fields = ('restaurant',)


@admin.register(TableZone)
class TableZoneAdmin(UnfoldModelAdmin):
    list_display = ('name', 'restaurant', 'sort_order', 'created_at')
    list_filter = ('restaurant',)
    search_fields = ('name', 'restaurant__name')
    autocomplete_fields = ('restaurant',)


@admin.register(Table)
class TableAdmin(UnfoldModelAdmin):
    list_display = ('name', 'restaurant', 'zone', 'seats', 'is_active', 'session_opened_at', 'sort_order')
    list_filter = ('is_active', 'restaurant')
    search_fields = ('name', 'restaurant__name')
    autocomplete_fields = ('restaurant', 'zone', 'waiters')
