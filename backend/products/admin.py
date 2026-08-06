from django.contrib import admin
from .models import (
    Category,
    Product,
    ProductVariant,
    ProductImage,
)


# =====================================================
# CATEGORY
# =====================================================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name",
    )

    ordering = (
        "name",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }


# =====================================================
# PRODUCT VARIANT INLINE
# =====================================================

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    ordering = ("weight",)


# =====================================================
# PRODUCT IMAGE INLINE
# =====================================================

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    ordering = ("display_order",)


# =====================================================
# PRODUCT
# =====================================================

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "category",
        "brand",
        "featured",
        "featured_order",
        "is_active",
    )

    list_filter = (
        "category",
        "featured",
        "is_active",
        "brand",
    )

    search_fields = (
        "name",
        "brand",
    )

    ordering = (
        "featured_order",
        "name",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }

    fieldsets = (

        (
            "Basic Information",
            {
                "fields": (
                    "category",
                    "name",
                    "slug",
                    "brand",
                )
            },
        ),

        (
            "Description",
            {
                "fields": (
                    "short_description",
                    "description",
                )
            },
        ),

        (
            "Homepage Settings",
            {
                "fields": (
                    "featured",
                    "featured_order",
                    "is_active",
                )
            },
        ),

    )

    inlines = [
        ProductVariantInline,
        ProductImageInline,
    ]


# =====================================================
# PRODUCT VARIANT
# =====================================================

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):

    list_display = (
        "product",
        "variant_name",
        "selling_price",
        "stock",
        "is_active",
    )

    list_filter = (
        "is_active",
        "unit",
    )

    search_fields = (
        "sku",
        "barcode",
        "product__name",
    )

    ordering = (
        "product",
        "weight",
    )


# =====================================================
# PRODUCT IMAGE
# =====================================================

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):

    list_display = (
        "product",
        "is_primary",
        "display_order",
    )

    list_filter = (
        "is_primary",
    )

    ordering = (
        "product",
        "display_order",
    )