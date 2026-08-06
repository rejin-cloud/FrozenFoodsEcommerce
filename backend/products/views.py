from django.shortcuts import render
from .models import Category, Product


def home(request):

    categories = Category.objects.filter(
        is_active=True
    ).order_by("name")

    featured_products = Product.objects.filter(
        is_active=True,
        featured=True
    ).order_by("featured_order")[:8]

    context = {
        "categories": categories,
        "featured_products": featured_products,
    }

    return render(
        request,
        "home/index.html",
        context,
    )