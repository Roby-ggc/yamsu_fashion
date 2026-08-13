from django.contrib import admin
from django.utils.html import format_html

from .models import Product, CustomerProfile, Order, OrderItem


# ==========================
# PRODUITS
# ==========================

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        'image_preview',
        'name',
        'category',
        'price',
        'stock',
        'available'
    )

    list_filter = (
        'category',
        'available'
    )

    search_fields = (
        'name',
        'category'
    )


    def image_preview(self, obj):

        if obj.image and hasattr(obj.image, 'url'):

            return format_html(
                '<img src="{}" width="60" height="60" style="object-fit:contain;border-radius:8px;">',
                obj.image.url
            )

        return "Pas d'image"


    image_preview.short_description = "Image"



# ==========================
# PROFIL CLIENT
# ==========================

@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'phone',
        'address'
    )

    search_fields = (
        'user__username',
        'phone'
    )



# ==========================
# PRODUITS DANS UNE COMMANDE
# ==========================

class OrderItemInline(admin.TabularInline):

    model = OrderItem

    extra = 0


    readonly_fields = (
        'image_preview',
        'product',
        'quantity',
        'size',
        'price'
    )


    def image_preview(self, obj):

        if obj.product and obj.product.image and hasattr(obj.product.image, 'url'):

            return format_html(
                '<img src="{}" width="60" height="60" style="object-fit:contain;border-radius:8px;">',
                obj.product.image.url
            )

        return "Pas d'image"


    image_preview.short_description = "Image"



# ==========================
# COMMANDES
# ==========================

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'full_name',
        'phone',
        'total',
        'status',
        'created_at'
    )


    list_filter = (
        'status',
        'created_at'
    )


    search_fields = (
        'full_name',
        'phone',
        'user__username'
    )


    inlines = [
        OrderItemInline
    ]



# ==========================
# ORDER ITEMS
# ==========================

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    list_display = (
        'image_preview',
        'order',
        'product',
        'quantity',
        'size',
        'price'
    )


    search_fields = (
        'product__name',
        'order__id'
    )


    def image_preview(self, obj):

        if obj.product and obj.product.image and hasattr(obj.product.image, 'url'):

            return format_html(
                '<img src="{}" width="60" height="60" style="object-fit:contain;border-radius:8px;">',
                obj.product.image.url
            )

        return "Pas d'image"


    image_preview.short_description = "Image"