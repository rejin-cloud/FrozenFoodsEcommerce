from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from orders.models import Order

def mock_payment_process(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "success":
            order.is_paid = True
            order.status = "Processing"
            order.save()

            # Deduct inventory stock on successful online payment
            for item in order.items.all():
                if item.variant:
                    item.variant.stock = max(0, item.variant.stock - item.quantity)
                    item.variant.save()

            messages.success(request, "Payment successful!")
            return redirect('orders:order_success', order_id=order.id)
        else:
            order.status = "Cancelled"
            order.save()
            messages.error(request, "Payment failed or was cancelled.")
            return redirect('orders:checkout')

    return render(request, 'payments/mock_payment.html', {'order': order})