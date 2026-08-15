from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.checkout_view, name='checkout'),
    path('success/<int:order_id>/', views.order_success, name='order_success'),
    path('order/<int:order_id>/pdf/', views.download_invoice_pdf, name='download_invoice_pdf'),
    path('track/<int:order_id>/', views.track_order, name='track_order'),
]