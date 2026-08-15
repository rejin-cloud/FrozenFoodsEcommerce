from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ("product_name", "variant_name", "price", "quantity")
    extra = 0


@admin.action(description="Mark selected orders as Paid & Completed")
def mark_as_completed(modeladmin, request, queryset):
    for order in queryset:
        order.is_paid = True
        order.save()  # Triggers the Order model's save() method to set status = 'Completed'


@admin.action(description="Mark selected orders as Cancelled")
def mark_as_cancelled(modeladmin, request, queryset):
    queryset.update(status="Cancelled")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "full_name",
        "total_amount",
        "payment_method",
        "is_paid",
        "status",
        "created_at",
    )
    list_filter = ("status", "payment_method", "is_paid", "created_at")
    search_fields = ("id", "full_name", "email", "phone")
    inlines = [OrderItemInline]
    actions = [mark_as_completed, mark_as_cancelled]