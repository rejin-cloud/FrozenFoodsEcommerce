from django.urls import path
from . import views

app_name = "adminpanel"


urlpatterns = [

    # Dashboard
    path(
        "",
        views.dashboard,
        name="dashboard"
    ),

    # Customers
    path(
        "customers/",
        views.customers,
        name="customers"
    ),

    # Products
    path(
        "products/",
        views.products,
        name="products"
    ),

    # Add Product
    path(
        "products/add/",
        views.add_product,
        name="add_product"
    ),

    # Edit Product
    path(
        "products/<int:product_id>/edit/",
        views.edit_product,
        name="edit_product"
    ),

    # Delete Product
    path(
        "products/<int:product_id>/delete/",
        views.delete_product,
        name="delete_product"
    ),

    # Categories
    path(
        "categories/",
        views.categories,
        name="categories"
    ),

    # Orders
    path(
        "orders/",
        views.orders,
        name="orders"
    ),

    # Cart
    path(
        "carts/",
        views.carts,
        name="carts"
    ),

    # Cart Items
    path(
        "cart-items/",
        views.cart_items,
        name="cart_items"
    ),

    # Product Images
    path(
        "product-images/",
        views.product_images,
        name="product_images"
    ),

    # Product Variants
    path(
        "product-variants/",
        views.product_variants,
        name="product_variants"
    ),
    # =====================================================
    # CATEGORIES
    # =====================================================

    path(
        "categories/",
        views.categories,
        name="categories"
    ),

    path(
        "categories/add/",
        views.add_category,
        name="add_category"
    ),

    path(
        "categories/<int:category_id>/edit/",
        views.edit_category,
        name="edit_category"
    ),

    path(
        "categories/<int:category_id>/delete/",
        views.delete_category,
        name="delete_category"
    ),

    path(
    "product-variants/add/",
    views.add_product_variant,
    name="add_product_variant"
    ),

    path(
    "orders/<int:order_id>/",
    views.order_detail,
    name="order_detail"
    ),

    path(
    "order-reports/",
    views.order_reports,
    name="order_reports"
    ),

]