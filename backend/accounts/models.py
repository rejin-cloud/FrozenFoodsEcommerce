from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.username or self.email


class UserAddress(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='addresses'
    )
    address_title = models.CharField(max_length=50, default="Home")  # e.g., Home, Work, Office
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_default', '-created_at']
        verbose_name_plural = "User Addresses"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Ensure only one address is set as default per user
        if self.is_default:
            UserAddress.objects.filter(user=self.user, is_default=True).exclude(pk=self.pk).update(is_default=False)

    def __str__(self):
        return f"{self.address_title} - {self.full_name} ({self.city})"