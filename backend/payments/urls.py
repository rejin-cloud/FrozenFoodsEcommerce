from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('mock/<int:order_id>/', views.mock_payment_process, name='mock_payment'),
]