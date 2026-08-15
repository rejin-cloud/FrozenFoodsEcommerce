from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from orders.models import Order
from .models import UserAddress
from .forms import UserRegisterForm, CustomUserUpdateForm


def register_view(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Account created successfully for {user.username}!")
            return redirect('/')
    else:
        form = UserRegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                next_url = request.GET.get('next') or '/'
                return redirect(next_url)
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('accounts:login')


@login_required
def profile_view(request):
    addresses = request.user.addresses.all()
    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your details have been updated successfully!")
            return redirect('accounts:profile')
    else:
        form = CustomUserUpdateForm(instance=request.user)

    return render(request, 'accounts/profile.html', {
        'form': form,
        'addresses': addresses,
    })


@login_required
def user_orders_view(request):
    """Renders the list of all orders for the logged-in user."""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'accounts/orders.html', {'orders': orders})


@login_required
def order_detail_view(request, order_id):
    """Renders the receipt/detail view for a single order."""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'accounts/order_detail.html', {'order': order})


# ==========================================
# Address Book Management Views
# ==========================================

@login_required
def manage_addresses_view(request):
    """View to add a saved delivery address and return to the profile page."""
    if request.method == 'POST':
        address_title = request.POST.get('address_title', 'Home')
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        is_default = request.POST.get('is_default') == 'on'

        UserAddress.objects.create(
            user=request.user,
            address_title=address_title,
            full_name=full_name,
            phone=phone,
            address=address,
            city=city,
            pincode=pincode,
            is_default=is_default
        )
        messages.success(request, "New address added successfully.")

    return redirect('accounts:profile')


@login_required
def delete_address_view(request, address_id):
    """View to delete a saved address."""
    address_obj = get_object_or_404(UserAddress, id=address_id, user=request.user)
    address_obj.delete()
    messages.success(request, "Address deleted successfully.")
    return redirect('accounts:profile')


@login_required
def set_default_address_view(request, address_id):
    """View to set a specific address as default."""
    address_obj = get_object_or_404(UserAddress, id=address_id, user=request.user)
    address_obj.is_default = True
    address_obj.save()
    messages.success(request, f"'{address_obj.address_title}' set as default address.")
    return redirect('accounts:profile')