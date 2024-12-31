from django.urls import path
from .import views

app_name = 'shop'

urlpatterns = [
    # 一般ユーザー用の商品ページ
    path('index/', views.ProductListView.as_view(), name='product_list'),
    path('detail/<int:pk>', views.ProductDetailView.as_view(), name='product_details'),

    # 管理者用の商品管理ページ 'admin/products/'
    path('list/', views.AdminProductListView.as_view(), name='admin_products_list'),
    path('create/', views.AdminProductCreateView.as_view(), name='admin_product_create'),
    path('', views.AdminProductListView.as_view(), name='admin_products_list'),
]