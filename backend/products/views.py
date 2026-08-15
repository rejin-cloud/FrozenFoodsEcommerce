from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Prefetch
from django.db.models import Sum
from orders.models import OrderItem

from .models import (
    Category,
    Product,
    Wishlist,
    ProductVariant,
)


# =========================================================
# HOME PAGE
# =========================================================

def home(request):

    # -----------------------------------------------------
    # ACTIVE CATEGORIES
    # -----------------------------------------------------

    categories = (
        Category.objects
        .filter(is_active=True)
        .order_by("name")
    )


    # -----------------------------------------------------
    # FEATURED PRODUCTS
    # -----------------------------------------------------

    featured_products = (
        Product.objects
        .filter(
            is_active=True,
            featured=True
        )
        .select_related("category")
        .prefetch_related(
            "variants",
            "images"
        )
        .order_by("featured_order")[:8]
    )


    # -----------------------------------------------------
    # POPULAR / BEST-SELLING PRODUCTS
    # -----------------------------------------------------
    #
    # Calculate how many units of each product have been sold.
    #
    # OrderItem -> ProductVariant -> Product
    #
    # Only count orders that are not cancelled.
    # -----------------------------------------------------

    sold_product_ids = (
        OrderItem.objects
        .exclude(
            order__status="Cancelled"
        )
        .values(
            "variant__product"
        )
        .annotate(
            total_sold=Sum("quantity")
        )
        .order_by(
            "-total_sold"
        )[:8]
    )


    # Get product IDs in popularity order
    popular_product_ids = [
        item["variant__product"]
        for item in sold_product_ids
    ]


    # Fetch the actual products
    popular_products_queryset = (
        Product.objects
        .filter(
            id__in=popular_product_ids,
            is_active=True
        )
        .select_related("category")
        .prefetch_related(
            "variants",
            "images"
        )
    )


    # Preserve the popularity order
    popular_products_dict = {
        product.id: product
        for product in popular_products_queryset
    }


    popular_products = [
        popular_products_dict[product_id]
        for product_id in popular_product_ids
        if product_id in popular_products_dict
    ]


    # -----------------------------------------------------
    # FALLBACK
    # -----------------------------------------------------
    #
    # If there are no completed/non-cancelled sales yet,
    # show active products instead.
    #
    # This prevents the Popular Products section from
    # being completely empty on a new website.
    # -----------------------------------------------------

    if not popular_products:

        popular_products = list(
            Product.objects
            .filter(
                is_active=True
            )
            .select_related("category")
            .prefetch_related(
                "variants",
                "images"
            )
            .order_by("-id")[:8]
        )


    # -----------------------------------------------------
    # USER WISHLIST
    # -----------------------------------------------------

    user_wishlist_ids = []

    if request.user.is_authenticated:

        user_wishlist_ids = list(
            Wishlist.objects
            .filter(
                user=request.user
            )
            .values_list(
                "product_id",
                flat=True
            )
        )

    special_offers = (
        Product.objects
        .filter(
            is_active=True,
            variants__is_active=True,
        )
        .prefetch_related(
            "variants",
            "images"
        )
        .distinct()
    )


    # -----------------------------------------------------
    # CONTEXT
    # -----------------------------------------------------

    context = {

        "categories": categories,

        "featured_products": featured_products,

        "popular_products": popular_products,

        "user_wishlist_ids": user_wishlist_ids,

        "special_offers": special_offers,

    }


    return render(
        request,
        "home/index.html",
        context,
    )


# =========================================================
# PRODUCT DETAIL
# =========================================================

def product_detail(request, slug):

    product = get_object_or_404(
        Product.objects.prefetch_related(
            "variants",
            "images"
        ),
        slug=slug,
        is_active=True,
    )


    # Active variants ordered by weight
    variants = (
        product.variants
        .filter(
            is_active=True
        )
        .order_by("weight")
    )


    # -----------------------------------------------------
    # RELATED PRODUCTS
    # -----------------------------------------------------

    related_products = (
        Product.objects
        .filter(
            category=product.category,
            is_active=True,
        )
        .exclude(
            id=product.id
        )
        .prefetch_related(
            "images"
        )[:4]
    )


    # -----------------------------------------------------
    # WISHLIST STATUS
    # -----------------------------------------------------

    is_in_wishlist = False

    if request.user.is_authenticated:

        is_in_wishlist = Wishlist.objects.filter(
            user=request.user,
            product=product
        ).exists()


    # -----------------------------------------------------
    # CONTEXT
    # -----------------------------------------------------

    context = {

        "product": product,

        "variants": variants,

        "related_products": related_products,

        "is_in_wishlist": is_in_wishlist,

    }


    return render(
        request,
        "products/detail.html",
        context,
    )


# =========================================================
# WISHLIST
# =========================================================

@login_required
def wishlist_view(request):

    wishlist_items = (
        Wishlist.objects
        .filter(
            user=request.user
        )
        .select_related(
            "product",
            "product__category"
        )
        .prefetch_related(
            "product__images",
            "product__variants"
        )
    )


    return render(
        request,
        "products/wishlist.html",
        {
            "wishlist_items": wishlist_items
        }
    )


# =========================================================
# TOGGLE WISHLIST
# =========================================================

@login_required
def toggle_wishlist_view(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )


    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )


    if not created:

        wishlist_item.delete()

        messages.info(
            request,
            f"Removed '{product.name}' from your wishlist."
        )

    else:

        messages.success(
            request,
            f"Added '{product.name}' to your wishlist!"
        )


    next_url = (
        request.META.get("HTTP_REFERER")
        or "products:wishlist"
    )


    return redirect(next_url)


# =========================================================
# REMOVE FROM WISHLIST
# =========================================================

@login_required
def remove_from_wishlist_view(request, product_id):

    Wishlist.objects.filter(
        user=request.user,
        product_id=product_id
    ).delete()


    messages.info(
        request,
        "Item removed from your wishlist."
    )


    return redirect(
        "products:wishlist"
    )


# =========================================================
# CATEGORY PRODUCTS
# =========================================================

def category_products(request, slug):

    category = get_object_or_404(
        Category,
        slug=slug
    )


    products = (
        Product.objects
        .filter(
            category=category
        )
        .prefetch_related(
            Prefetch(
                "variants",
                queryset=(
                    ProductVariant.objects
                    .filter(
                        is_active=True
                    )
                    .order_by("weight")
                ),
                to_attr="sorted_variants"
            ),
            "images"
        )
        .order_by(
            "-featured",
            "name"
        )
    )


    return render(
        request,
        "products/category_products.html",
        {
            "category": category,
            "products": products,
        }
    )