from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Order
from .utils import send_order_confirmation_email, send_order_status_email

@receiver(pre_save, sender=Order)
def cache_previous_order_status(sender, instance, **kwargs):
    """Track the previous status before saving to detect changes."""
    if instance.pk:
        try:
            previous_instance = Order.objects.get(pk=instance.pk)
            instance._previous_status = previous_instance.status
        except Order.DoesNotExist:
            instance._previous_status = None
    else:
        instance._previous_status = None

@receiver(post_save, sender=Order)
def trigger_order_email_notifications(sender, instance, created, **kwargs):
    """Trigger emails on order creation or status changes."""
    if created:
        send_order_confirmation_email(instance)
    else:
        previous_status = getattr(instance, '_previous_status', None)
        if previous_status and previous_status != instance.status:
            send_order_status_email(instance)   