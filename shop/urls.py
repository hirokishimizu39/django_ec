from django.urls import path
from .import views

app_name = 'shop'

urlpatterns = [
    # 一般ユーザー用の商品ページ
    path('index/', views.ProductListView.as_view(), name='product_list'),
    path('detail/<int:pk>', views.ProductDetailView.as_view(), name='product_details'),



    path('', views.ProductListView.as_view(), name='product_list'),
]