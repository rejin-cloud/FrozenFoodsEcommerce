from django.urls import path

from . import views

urlpatterns = [

    path(
        "add/",
        views.add_to_cart,
        name="add_to_cart",
    ),

    path(
        "",
        views.cart_view,
        name="cart",
    ),

    path(
    "update/",
    views.update_cart,
    name="update_cart",
    ),

    path(
    "remove/",
    views.remove_cart_item,
    name="remove_cart_item",
    ),

]