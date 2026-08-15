from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from .models import Cart, CartItem
from products.models import ProductVariant


@require_POST
def add_to_cart(request):
    variant_id = request.POST.get("variant_id")
    quantity_raw = request.POST.get("quantity", 1)

    # 1. Check if variant_id was sent from front-end
    if not variant_id:
        return JsonResponse(
            {"success": False, "message": "Please select a size/variant first."},
            status=400,
        )

    # 2. Safely fetch the ProductVariant
    try:
        quantity = int(quantity_raw)
        variant = ProductVariant.objects.get(id=variant_id)
    except (ValueError, ProductVariant.DoesNotExist):
        return JsonResponse(
            {"success": False, "message": "Invalid product variant selected."},
            status=400,
        )

    # 3. Check if variant is completely out of stock
    if variant.stock <= 0:
        return JsonResponse(
            {"success": False, "message": "Sorry, this product is out of stock."},
            status=400,
        )

    # 4. Get or create Cart safely without crashing on duplicates
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        if not cart:
            cart = Cart.objects.create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        cart = Cart.objects.filter(session_key=session_key).first()
        if not cart:
            cart = Cart.objects.create(session_key=session_key)

    # 5. Check existing item quantity in cart against available stock
    existing_item = CartItem.objects.filter(cart=cart, variant=variant).first()
    current_qty_in_cart = existing_item.quantity if existing_item else 0

    if (current_qty_in_cart + quantity) > variant.stock:
        return JsonResponse(
            {
                "success": False,
                "message": f"Cannot add. You have {current_qty_in_cart} in cart and total stock is only {variant.stock}.",
            },
            status=400,
        )

    # 6. Add item or update quantity safely
    if existing_item:
        existing_item.quantity += quantity
        existing_item.save()
    else:
        CartItem.objects.create(
            cart=cart,
            variant=variant,
            price=variant.selling_price,
            quantity=quantity,
        )

    # Safely get cart count
    cart_count = getattr(
        cart, "total_items", sum(i.quantity for i in cart.items.all())
    )

    return JsonResponse(
        {
            "success": True,
            "cart_count": cart_count,
            "message": "Product added successfully.",
        }
    )


def cart_view(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        cart = Cart.objects.filter(
            session_key=request.session.session_key
        ).first()

    if cart:
        items = cart.items.select_related("variant", "variant__product")
        # Automatically clamp cart quantity if available stock is lower than current cart quantity
        for item in items:
            if item.variant and item.quantity > item.variant.stock:
                if item.variant.stock <= 0:
                    item.delete()
                else:
                    item.quantity = item.variant.stock
                    item.save()
    else:
        items = []

    total = sum(item.subtotal for item in items)

    return render(
        request,
        "cart/cart.html",
        {
            "items": items,
            "total": total,
        },
    )


@require_POST
def update_cart(request):
    item_id = request.POST.get("item_id")
    action = request.POST.get("action")

    try:
        item = CartItem.objects.select_related("variant").get(id=item_id)
    except CartItem.DoesNotExist:
        return JsonResponse(
            {"success": False, "message": "Item not found."}, status=404
        )

    if action == "increase":
        # Validate that incrementing does not exceed the available stock
        if item.variant and item.quantity >= item.variant.stock:
            return JsonResponse(
                {
                    "success": False,
                    "message": f"Cannot add more. Maximum available stock is {item.variant.stock}.",
                },
                status=400,
            )
        item.quantity += 1
    elif action == "decrease":
        if item.quantity > 1:
            item.quantity -= 1

    item.save()
    cart = item.cart
    total = sum(i.subtotal for i in cart.items.all())

    cart_count = getattr(
        cart, "total_items", sum(i.quantity for i in cart.items.all())
    )

    return JsonResponse(
        {
            "success": True,
            "quantity": item.quantity,
            "subtotal": float(item.subtotal),
            "total": float(total),
            "cart_count": cart_count,
        }
    )


@require_POST
def remove_cart_item(request):
    item_id = request.POST.get("item_id")

    try:
        item = CartItem.objects.get(id=item_id)
        cart = item.cart
        item.delete()
    except CartItem.DoesNotExist:
        return JsonResponse(
            {"success": False, "message": "Item not found."}, status=404
        )

    total = sum(i.subtotal for i in cart.items.all())
    cart_count = getattr(
        cart, "total_items", sum(i.quantity for i in cart.items.all())
    )

    return JsonResponse(
        {
            "success": True,
            "total": float(total),
            "cart_count": cart_count,
        }
    )