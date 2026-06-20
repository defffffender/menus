from django.contrib import admin

from .models import Membership, MenuTheme, Restaurant, Table, TableZone


class MembershipInline(admin.TabularInline):
    model = Membership
    extra = 1
    autocomplete_fields = ('user',)


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'city', 'owner', 'is_active', 'created_at')
    list_filter = ('type', 'is_active', 'city')
    search_fields = ('name', 'slug', 'phone')
    prepopulated_fields = {'slug': ('name',)}
    autocomplete_fields = ('owner',)
    inlines = (MembershipInline,)


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'restaurant', 'role', 'is_active', 'created_at')
    list_filter = ('role', 'is_active')
    search_fields = ('user__phone', 'user__full_name', 'restaurant__name')
    autocomplete_fields = ('user', 'restaurant')


@admin.register(MenuTheme)
class MenuThemeAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'font', 'card_style', 'updated_at')
    search_fields = ('restaurant__name',)
    autocomplete_fields = ('restaurant',)


@admin.register(TableZone)
class TableZoneAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant', 'sort_order', 'created_at')
    list_filter = ('restaurant',)
    search_fields = ('name', 'restaurant__name')
    autocomplete_fields = ('restaurant',)


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant', 'zone', 'seats', 'is_active', 'sort_order')
    list_filter = ('is_active', 'restaurant')
    search_fields = ('name', 'restaurant__name')
    autocomplete_fields = ('restaurant', 'zone', 'waiters')
