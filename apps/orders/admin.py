from django.contrib import admin
from unfold.admin import ModelAdmin as UnfoldModelAdmin
from unfold.admin import TabularInline as UnfoldTabularInline

from .models import Order, OrderItem


class OrderItemInline(UnfoldTabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('name', 'price', 'quantity', 'variant')
    can_delete = False


@admin.register(Order)
class OrderAdmin(UnfoldModelAdmin):
    list_display = ('pk', 'restaurant', 'table', 'status', 'created_at')
    list_filter = ('status', 'restaurant')
    search_fields = ('pk', 'restaurant__name')
    readonly_fields = ('public_token', 'created_at', 'updated_at')
    inlines = (OrderItemInline,)


@admin.register(OrderItem)
class OrderItemAdmin(UnfoldModelAdmin):
    list_display = ('order', 'name', 'price', 'quantity')
    search_fields = ('name', 'order__pk')
