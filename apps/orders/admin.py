from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('name', 'price', 'quantity', 'variant')
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('pk', 'restaurant', 'table', 'status', 'created_at')
    list_filter = ('status', 'restaurant')
    search_fields = ('pk', 'restaurant__name')
    readonly_fields = ('public_token', 'created_at', 'updated_at')
    inlines = (OrderItemInline,)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'name', 'price', 'quantity')
    search_fields = ('name', 'order__pk')
