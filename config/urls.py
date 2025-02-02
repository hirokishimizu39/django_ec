"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from shop import views

urlpatterns = [
    # 管理者用の商品管理ページ 'admin/products/'
    path('admin/products/list/', views.AdminProductListView.as_view(), name='admin_products_list'),
    path('admin/products/create/', views.AdminProductCreateView.as_view(), name='admin_product_create'),
    path('admin/products/edit/<int:pk>/', views.AdminProductUpdateView.as_view(), name='admin_product_edit'),
    path('admin/products/delete/<int:pk>/', views.AdminProductDeleteView.as_view(), name='admin_product_delete'),

    # django標準の管理者機能
    path('admin/', admin.site.urls),

    path('hello/', TemplateView.as_view(template_name='hello.html')),
    path('cart/', include('cart.urls')),
    path('promotion/', include('promotion.urls')),
    path('order/', include('order.urls')),
    path('', include('shop.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls))
    ]