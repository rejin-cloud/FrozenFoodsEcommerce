from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.contrib import messages
from django.db import transaction
from cart.models import Cart
from .models import Order, OrderItem
from accounts.models import UserAddress
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from xhtml2pdf import pisa


def get_active_cart(request):
    if request.user.is_authenticated:
        return Cart.objects.filter(user=request.user).first()
    
    session_key = request.session.session_key
    if session_key:
        return Cart.objects.filter(session_key=session_key).first()
    return None


@transaction.atomic
def checkout_view(request):
    cart = get_active_cart(request)

    if not cart or not cart.items.exists():
        messages.warning(request, "Your cart is empty.")
        return redirect('cart')

    items = cart.items.select_related('variant__product').all()
    total = cart.total_amount

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method', 'COD')
        selected_address_id = request.POST.get('selected_address_id')

        chosen_address_obj = None

        # 1. Determine address details (Selected saved address vs manually entered)
        if selected_address_id and request.user.is_authenticated:
            chosen_address_obj = get_object_or_404(UserAddress, id=selected_address_id, user=request.user)
            full_name = chosen_address_obj.full_name
            email = request.user.email
            phone = chosen_address_obj.phone
            address = chosen_address_obj.address
            city = chosen_address_obj.city
            pincode = chosen_address_obj.pincode
        else:
            full_name = request.POST.get('full_name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            address = request.POST.get('address')
            city = request.POST.get('city')
            pincode = request.POST.get('pincode')

        # 2. Create Order
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            saved_address=chosen_address_obj,
            full_name=full_name,
            email=email,
            phone=phone,
            address=address,
            city=city,
            pincode=pincode,
            total_amount=total,
            payment_method=payment_method,
            status='Pending'
        )

        # 3. Add Items to Order
        for item in items:
            OrderItem.objects.create(
                order=order,
                variant=item.variant,
                product_name=item.variant.product.name,
                variant_name=item.variant.variant_name,
                price=item.price,
                quantity=item.quantity
            )

            # Deduct stock immediately if Cash on Delivery
            if payment_method == 'COD' and item.variant:
                item.variant.stock = max(0, item.variant.stock - item.quantity)
                item.variant.save()

        # 4. Clear Cart
        cart.items.all().delete()

        # 5. Route based on Payment Method
        if payment_method == 'COD':
            return redirect('orders:order_success', order_id=order.id)
        
        elif payment_method == 'ONLINE_MOCK':
            return redirect('payments:mock_payment', order_id=order.id)

    # Fetch user addresses and initial fallback data
    user_addresses = []
    initial_data = {}

    if request.user.is_authenticated:
        u = request.user
        user_addresses = u.addresses.all()

        initial_data = {
            'full_name': f"{u.first_name} {u.last_name}".strip() or u.username,
            'email': u.email or '',
            'phone': getattr(u, 'phone_number', ''),
            'address': getattr(u, 'address', ''),
            'city': getattr(u, 'city', ''),
            'pincode': getattr(u, 'pincode', ''),
        }

    return render(request, 'checkout/checkout.html', {
        'items': items,
        'total': total,
        'initial_data': initial_data,
        'user_addresses': user_addresses,
    })


def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if order.payment_method == 'ONLINE_MOCK' and not order.is_paid:
        order.is_paid = True

        for item in order.items.all():
            if item.variant:
                item.variant.stock = max(0, item.variant.stock - item.quantity)
                item.variant.save()

        order.save()

    return render(request, 'checkout/success.html', {'order': order})


def download_invoice_pdf(request, order_id):
    """Generates and serves a downloadable PDF invoice for an order."""
    if request.user.is_authenticated:
        order = get_object_or_404(Order, id=order_id, user=request.user)
    else:
        order = get_object_or_404(Order, id=order_id)

    context = {'order': order}
    html_string = render_to_string('orders/pdf_invoice.html', context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Invoice_Order_{order.id}.pdf"'

    pisa_status = pisa.CreatePDF(html_string, dest=response)
    if pisa_status.err:
        return HttpResponse('Error generating PDF invoice', status=500)

    return response


@login_required
def track_order(request, order_id):
    """Renders a dedicated tracking page for a specific order."""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "orders/track_order.html", {"order": order})