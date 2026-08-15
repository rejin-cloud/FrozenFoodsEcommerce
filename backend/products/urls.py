from django.urls import path
from . import views

app_name = "products"

urlpatterns = [

    path(
        "wishlist/",
        views.wishlist_view,
        name="wishlist"
    ),

    path(
        "wishlist/toggle/<int:product_id>/",
        views.toggle_wishlist_view,
        name="toggle_wishlist"
    ),

    path(
        "wishlist/remove/<int:product_id>/",
        views.remove_from_wishlist_view,
        name="remove_from_wishlist"
    ),

    # Category products
    path(
        "category/<slug:slug>/",
        views.category_products,
        name="category_products"
    ),

    # Product detail
    path(
        "<slug:slug>/",
        views.product_detail,
        name="product_detail"
    ),

]