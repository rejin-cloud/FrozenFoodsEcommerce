import csv

from datetime import timedelta

from django.http import HttpResponse
from django.utils import timezone

from django.db.models import Sum

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib import messages

from accounts.models import CustomUser
from products.models import (
    Product,
    ProductVariant,
    Category,
    ProductImage,
)
from cart.models import Cart, CartItem
from orders.models import Order

from .forms import ProductForm, CategoryForm, ProductVariantForm

User = get_user_model()


def dashboard(request):

    # Customer count
    customer_count = User.objects.count()

    # Product count
    product_count = Product.objects.count()

    # Category count
    category_count = Category.objects.count()

    # Variant count
    variant_count = ProductVariant.objects.count()

    # Cart count
    cart_count = Cart.objects.count()

    # Cart item count
    cart_item_count = CartItem.objects.count()

    # Order count
    order_count = Order.objects.count()

    context = {
        "customer_count": customer_count,
        "product_count": product_count,
        "category_count": category_count,
        "variant_count": variant_count,
        "cart_count": cart_count,
        "cart_item_count": cart_item_count,
        "order_count": order_count,
    }

    return render(
        request,
        "adminpanel/dashboard.html",
        context
    )


def products(request):

    products = Product.objects.all().order_by("-id")

    return render(
        request,
        "adminpanel/products.html",
        {
            "products": products,
        }
    )


def categories(request):

    categories = Category.objects.all().order_by("name")

    return render(
        request,
        "adminpanel/categories.html",
        {
            "categories": categories,
        }
    )


def customers(request):

    customers = User.objects.all().order_by("-id")

    return render(
        request,
        "adminpanel/customers.html",
        {
            "customers": customers,
        }
    )


def orders(request):

    orders = Order.objects.all().order_by("-id")

    return render(
        request,
        "adminpanel/orders.html",
        {
            "orders": orders,
        }
    )


@staff_member_required
def carts(request):

    carts = Cart.objects.select_related("user").all().order_by("-id")

    return render(
        request,
        "adminpanel/carts.html",
        {
            "carts": carts,
        }
    )


@staff_member_required
def cart_items(request):

    cart_items = CartItem.objects.select_related(
        "cart",
        "variant",
        "variant__product"
    ).all().order_by("-id")

    return render(
        request,
        "adminpanel/cart_items.html",
        {
            "cart_items": cart_items,
        }
    )


@staff_member_required
def product_images(request):

    images = ProductImage.objects.select_related(
        "product"
    ).all().order_by("-id")

    return render(
        request,
        "adminpanel/product_images.html",
        {
            "images": images,
        }
    )


@staff_member_required
def product_variants(request):

    variants = ProductVariant.objects.select_related(
        "product"
    ).all().order_by("product", "weight")

    return render(
        request,
        "adminpanel/product_variants.html",
        {
            "variants": variants,
        }
    )


@staff_member_required
def add_product(request):

    if request.method == "POST":

        form = ProductForm(request.POST)

        if form.is_valid():

            product = form.save()

            messages.success(
                request,
                f'Product "{product.name}" was added successfully.'
            )

            return redirect("adminpanel:products")

    else:

        form = ProductForm()

    return render(
        request,
        "adminpanel/add_product.html",
        {
            "form": form,
        }
    )


# =========================================================
# EDIT PRODUCT
# =========================================================

@staff_member_required
def edit_product(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    if request.method == "POST":

        form = ProductForm(
            request.POST,
            instance=product
        )

        if form.is_valid():

            product = form.save()

            messages.success(
                request,
                f'Product "{product.name}" was updated successfully.'
            )

            return redirect("adminpanel:products")

    else:

        form = ProductForm(
            instance=product
        )

    return render(
        request,
        "adminpanel/edit_product.html",
        {
            "form": form,
            "product": product,
        }
    )


# =========================================================
# DELETE PRODUCT
# =========================================================

@staff_member_required
def delete_product(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    if request.method == "POST":

        product_name = product.name

        product.delete()

        messages.success(
            request,
            f'Product "{product_name}" was deleted successfully.'
        )

        return redirect("adminpanel:products")

    return render(
        request,
        "adminpanel/delete_product.html",
        {
            "product": product,
        }
    )

# =========================================================
# ADD CATEGORY
# =========================================================

@staff_member_required
def add_category(request):

    if request.method == "POST":

        form = CategoryForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            category = form.save()

            messages.success(
                request,
                f'Category "{category.name}" was added successfully.'
            )

            return redirect("adminpanel:categories")

    else:

        form = CategoryForm()

    return render(
        request,
        "adminpanel/add_category.html",
        {
            "form": form,
        }
    )


# =========================================================
# EDIT CATEGORY
# =========================================================

@staff_member_required
def edit_category(request, category_id):

    category = Category.objects.get(id=category_id)

    if request.method == "POST":

        form = CategoryForm(
            request.POST,
            request.FILES,
            instance=category
        )

        if form.is_valid():

            category = form.save()

            messages.success(
                request,
                f'Category "{category.name}" was updated successfully.'
            )

            return redirect("adminpanel:categories")

    else:

        form = CategoryForm(
            instance=category
        )

    return render(
        request,
        "adminpanel/edit_category.html",
        {
            "form": form,
            "category": category,
        }
    )


# =========================================================
# DELETE CATEGORY
# =========================================================

@staff_member_required
def delete_category(request, category_id):

    category = Category.objects.get(id=category_id)

    if request.method == "POST":

        category_name = category.name

        category.delete()

        messages.success(
            request,
            f'Category "{category_name}" was deleted successfully.'
        )

        return redirect("adminpanel:categories")

    return render(
        request,
        "adminpanel/delete_category.html",
        {
            "category": category,
        }
    )

@staff_member_required
def add_product_variant(request):

    if request.method == "POST":

        form = ProductVariantForm(request.POST)

        if form.is_valid():

            variant = form.save()

            messages.success(
                request,
                f'Variant "{variant.variant_name}" was added successfully.'
            )

            return redirect("adminpanel:product_variants")

    else:

        form = ProductVariantForm()

    return render(
        request,
        "adminpanel/add_product_variant.html",
        {
            "form": form,
        }
    )

# =========================================================
# ORDER DETAILS + UPDATE STATUS
# =========================================================

@staff_member_required
def order_detail(request, order_id):

    order = get_object_or_404(
        Order.objects.select_related(
            "user",
            "saved_address"
        ).prefetch_related(
            "items__variant",
            "items__variant__product"
        ),
        id=order_id
    )

    if request.method == "POST":

        new_status = request.POST.get("status")

        valid_statuses = dict(Order.STATUS_CHOICES)

        if new_status in valid_statuses:

            order.status = new_status
            order.save(update_fields=["status", "updated_at"])

            messages.success(
                request,
                f"Order #{order.id} status updated to {order.get_status_display()}."
            )

            return redirect(
                "adminpanel:order_detail",
                order_id=order.id
            )

        else:

            messages.error(
                request,
                "Invalid order status."
            )

    return render(
        request,
        "adminpanel/order_detail.html",
        {
            "order": order,
            "status_choices": Order.STATUS_CHOICES,
        }
    )

# =========================================================
# ORDER REPORTS
# =========================================================

@staff_member_required
def order_reports(request):

    today = timezone.localdate()

    period = request.GET.get("period", "today")

    # Default dates
    start_date = today
    end_date = today

    # -----------------------------
    # REPORT PERIOD
    # -----------------------------

    if period == "today":

        start_date = today
        end_date = today

        period_name = "Today"

    elif period == "yesterday":

        start_date = today - timedelta(days=1)
        end_date = start_date

        period_name = "Yesterday"

    elif period == "7days":

        start_date = today - timedelta(days=6)
        end_date = today

        period_name = "Last 7 Days"

    elif period == "30days":

        start_date = today - timedelta(days=29)
        end_date = today

        period_name = "Last 30 Days"

    elif period == "month":

        start_date = today.replace(day=1)
        end_date = today

        period_name = "This Month"

    else:

        start_date = today
        end_date = today

        period_name = "Today"

    # -----------------------------
    # FILTER ORDERS
    # -----------------------------

    orders = Order.objects.filter(
        created_at__date__gte=start_date,
        created_at__date__lte=end_date
    ).prefetch_related(
        "items"
    ).order_by("-created_at")

    # -----------------------------
    # TOTAL ORDERS
    # -----------------------------

    total_orders = orders.count()

    # -----------------------------
    # TOTAL REVENUE
    # -----------------------------

    total_revenue = sum(
        order.total_amount
        for order in orders
    )

    # -----------------------------
    # TOTAL ITEMS SOLD
    # -----------------------------

    items_sold = sum(
        item.quantity
        for order in orders
        for item in order.items.all()
    )

    # -----------------------------
    # AVERAGE ORDER VALUE
    # -----------------------------

    if total_orders > 0:

        average_order_value = (
            total_revenue / total_orders
        )

    else:

        average_order_value = 0

    # -----------------------------
    # CONTEXT
    # -----------------------------

    context = {

        "orders": orders,

        "period": period,

        "period_name": period_name,

        "start_date": start_date,

        "end_date": end_date,

        "total_orders": total_orders,

        "total_revenue": total_revenue,

        "average_order_value": average_order_value,

        "items_sold": items_sold,

    }

    return render(
        request,
        "adminpanel/order_reports.html",
        context
    )