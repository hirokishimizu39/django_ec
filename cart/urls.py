from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    # cart/ の後に続くurl
    path('add/<int:product_id>/', views.add_to_cart_view, name='add_to_cart'),
    path('remove/<int:product_id>/', views.remove_from_cart_view, name='remove_from_cart'),
    path('', views.cart_view, name='cart_view'),
]