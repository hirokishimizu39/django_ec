from django.urls import path
from . import views

app_name = 'shop'
urlpatterns = [
    path('index/', views.ProductListView.as_view(), name='product_list'),
    path('detail/<int:pk>', views.ProductDetailView.as_view(), name='product_details'),
    path('admin/products', views.AdminProductListView.as_view(), name='admin_products_list'),
    path('', views.ProductListView.as_view(), name='product_list'),
]