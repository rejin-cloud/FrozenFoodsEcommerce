from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from products.views import home

admin.site.site_header = "Meami.in Administration"
admin.site.site_title = "Meami.in Admin Portal"
admin.site.index_title = "Dashboard Management"

urlpatterns = [
    path('admin/', admin.site.urls),

    # Homepage & Products
    path('', home, name='home'),
    path('products/', include('products.urls')),

    # E-commerce Apps
    path('accounts/', include('accounts.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
    path('payments/', include('payments.urls')),
    path(
    "admin-dashboard/",
    include("adminpanel.urls")
    ),
    # path('dashboard/', include('dashboard.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)