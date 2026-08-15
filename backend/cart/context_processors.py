from .models import Cart


def cart_count(request):

    cart = None

    if request.user.is_authenticated:

        cart = Cart.objects.filter(
            user=request.user
        ).first()

    else:

        if request.session.session_key:

            cart = Cart.objects.filter(
                session_key=request.session.session_key
            ).first()

    return {

        "cart_count": cart.total_items if cart else 0

    }