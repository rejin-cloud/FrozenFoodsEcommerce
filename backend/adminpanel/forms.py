from django import forms
from django.utils.text import slugify

from products.models import Product, Category, ProductVariant


# =========================================================
# PRODUCT FORM
# =========================================================

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product

        fields = [
            "category",
            "name",
            "slug",
            "short_description",
            "description",
            "brand",
            "featured",
            "featured_order",
            "is_active",
        ]

        widgets = {

            "category": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter product name"
                }
            ),

            "slug": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "product-slug"
                }
            ),

            "short_description": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Short description"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 6,
                    "placeholder": "Enter full product description"
                }
            ),

            "brand": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Brand name"
                }
            ),

            "featured": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input"
                }
            ),

            "featured_order": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0"
                }
            ),

            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input"
                }
            ),
        }

        labels = {
            "category": "Category",
            "name": "Product Name",
            "slug": "Slug",
            "short_description": "Short Description",
            "description": "Description",
            "brand": "Brand",
            "featured": "Featured Product",
            "featured_order": "Featured Order",
            "is_active": "Active",
        }

    def clean_slug(self):
        slug = self.cleaned_data.get("slug")

        if not slug:
            name = self.cleaned_data.get("name")

            if name:
                slug = slugify(name)

        return slug


# =========================================================
# CATEGORY FORM
# =========================================================

class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category

        fields = [
            "name",
            "slug",
            "image",
            "description",
            "is_active",
        ]

        widgets = {

            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter category name"
                }
            ),

            "slug": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "category-slug"
                }
            ),

            "image": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": "image/*"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Enter category description"
                }
            ),

            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input"
                }
            ),
        }

        labels = {
            "name": "Category Name",
            "slug": "Slug",
            "image": "Category Image",
            "description": "Description",
            "is_active": "Active",
        }

    def clean_slug(self):
        slug = self.cleaned_data.get("slug")

        if not slug:
            name = self.cleaned_data.get("name")

            if name:
                slug = slugify(name)

        return slug

# ==========================================================
# PRODUCT VARIANT FORM
# ==========================================================

class ProductVariantForm(forms.ModelForm):

    class Meta:
        model = ProductVariant

        fields = [
            "product",
            "variant_name",
            "sku",
            "barcode",
            "weight",
            "unit",
            "mrp",
            "selling_price",
            "cost_price",
            "stock",
            "low_stock_alert",
            "is_active",
        ]

        widgets = {

            "product": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "variant_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Example: 500g, 1kg, Large"
                }
            ),

            "sku": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Example: CHICK1000"
                }
            ),

            "barcode": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Barcode (optional)"
                }
            ),

            "weight": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Example: 1",
                    "step": "0.01",
                    "min": "0"
                }
            ),

            "unit": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "mrp": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "MRP",
                    "step": "0.01",
                    "min": "0"
                }
            ),

            "selling_price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Selling price",
                    "step": "0.01",
                    "min": "0"
                }
            ),

            "cost_price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Cost price (optional)",
                    "step": "0.01",
                    "min": "0"
                }
            ),

            "stock": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Available stock",
                    "min": "0"
                }
            ),

            "low_stock_alert": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Example: 10",
                    "min": "0"
                }
            ),

            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input"
                }
            ),
        }

        labels = {
            "product": "Product",
            "variant_name": "Variant Name",
            "sku": "SKU",
            "barcode": "Barcode",
            "weight": "Weight",
            "unit": "Unit",
            "mrp": "MRP",
            "selling_price": "Selling Price",
            "cost_price": "Cost Price",
            "stock": "Stock",
            "low_stock_alert": "Low Stock Alert",
            "is_active": "Active",
        }