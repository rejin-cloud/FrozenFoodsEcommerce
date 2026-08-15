from django.db import models
from django.utils.text import slugify
from django.conf import settings


# ==========================
# Category
# ==========================

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    image = models.ImageField(upload_to="categories/")
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


# ==========================
# Product
# ==========================

class Product(models.Model):

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products"
    )

    name = models.CharField(max_length=200)

    slug = models.SlugField(
        max_length=220,
        unique=True,
        blank=True
    )

    short_description = models.CharField(
        max_length=300,
        blank=True
    )

    description = models.TextField()

    featured = models.BooleanField(default=False)

    featured_order = models.PositiveIntegerField(default=0)

    brand = models.CharField(
        max_length=100,
        blank=True
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["featured_order", "name"]

    def __str__(self):
        return self.name

    @property
    def primary_image(self):
        """
        Returns the primary product image.
        """
        return self.images.filter(is_primary=True).first()

    @property
    def primary_variant(self):
        """
        Returns the cheapest active variant.
        """
        return (
            self.variants
            .filter(is_active=True)
            .order_by("selling_price")
            .first()
        )

    @property
    def starting_price(self):
        variant = self.primary_variant
        return variant.selling_price if variant else None

    @property
    def mrp_price(self):
        variant = self.primary_variant
        return variant.mrp if variant else None

    @property
    def discount_percentage(self):
        variant = self.primary_variant

        if (
            variant
            and variant.mrp
            and variant.mrp > variant.selling_price
        ):
            return round(
                ((variant.mrp - variant.selling_price) / variant.mrp) * 100
            )

        return 0

    @property
    def is_in_stock(self):
        """
        Checks if any active variant has stock available.
        """
        return self.variants.filter(is_active=True, stock__gt=0).exists()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)


# ==========================
# Product Variant
# ==========================

class ProductVariant(models.Model):

    UNIT_CHOICES = [
        ("g", "Gram"),
        ("kg", "Kilogram"),
        ("ml", "Millilitre"),
        ("l", "Litre"),
        ("pc", "Piece"),
        ("pack", "Pack"),
    ]

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="variants"
    )

    variant_name = models.CharField(
        max_length=100,
        help_text="Example: 500g, 1kg, Large"
    )

    sku = models.CharField(
        max_length=50,
        unique=True
    )

    barcode = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    weight = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    unit = models.CharField(
        max_length=10,
        choices=UNIT_CHOICES
    )

    mrp = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    selling_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    cost_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    stock = models.PositiveIntegerField(default=0)

    low_stock_alert = models.PositiveIntegerField(default=10)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["product", "weight"]
        unique_together = ("product", "variant_name")

    def __str__(self):
        return f"{self.product.name} - {self.variant_name}"


# ==========================
# Product Images
# ==========================

class ProductImage(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(
        upload_to="products/gallery/"
    )

    alt_text = models.CharField(
        max_length=255,
        blank=True
    )

    is_primary = models.BooleanField(
        default=False,
        help_text="Use this image as the main product image."
    )

    display_order = models.PositiveIntegerField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["display_order"]

    def __str__(self):
        return f"{self.product.name} Image {self.display_order}"


# ==========================
# Wishlist / Saved Items
# ==========================

class Wishlist(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="wishlist_items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="in_wishlists"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]
        unique_together = ("user", "product")

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"