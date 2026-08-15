from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def send_order_confirmation_email(order):
    """Sends an HTML confirmation email when a new order is placed."""
    subject = f"Order Confirmation #{order.id} - FrozenFoods"
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@frozenfoods.com')
    to_email = [order.email]

    context = {'order': order}
    html_content = render_to_string('emails/order_confirmation.html', context)
    text_content = strip_tags(html_content)

    msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    msg.attach_alternative(html_content, "text/html")
    msg.send(fail_silently=True)

def send_order_status_email(order):
    """Sends an HTML update email when an order status changes."""
    subject = f"Update on Order #{order.id}: Status is now '{order.status}'"
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@frozenfoods.com')
    to_email = [order.email]

    context = {'order': order}
    html_content = render_to_string('emails/order_status_update.html', context)
    text_content = strip_tags(html_content)

    msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    msg.attach_alternative(html_content, "text/html")
    msg.send(fail_silently=True)