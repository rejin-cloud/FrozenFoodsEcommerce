from django.db import models
from django.conf import settings

from products.models import ProductVariant


class Cart(models.Model):
    """
    Shopping cart.
    Can belong to a logged-in user or a guest session.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="carts"
    )

    session_key = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        if self.user:
            return f"Cart - {self.user.username}"
        return f"Guest Cart - {self.session_key}"

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    @property
    def total_amount(self):
        return sum(item.subtotal for item in self.items.all())


class CartItem(models.Model):
    """
    Individual item inside the cart.
    """

    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items"
    )

    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        related_name="cart_items"
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        unique_together = ("cart", "variant")

    def __str__(self):
        return f"{self.variant.product.name} ({self.variant.variant_name})"

    @property
    def subtotal(self):
        return self.price * self.quantity