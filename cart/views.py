from django.shortcuts import render, redirect, get_object_or_404
from .utils import get_or_create_cart, add_to_cart, remove_from_cart
from shop.models import Product
from django.db.models import Sum


def add_to_cart_view(request, product_id):
    """商品をカートに追加するビュー"""
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    add_to_cart(request, product, quantity)
    return redirect('shop:product_list')

def remove_from_cart_view(request, product_id):
    """カートから商品を削除するビュー"""
    product = get_object_or_404(Product, id=product_id)
    remove_from_cart(request, product)
    return redirect('cart:cart_view')

def cart_view(request):
    """カートの中身を表示するビュー"""
    cart = get_or_create_cart(request)
    items = cart.items.select_related('product')
    product_quantities_in_cart_items = items.aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0
    total_price = cart.totalCartItemPrice()
    return render(request, 'cart/cart.html', {
        'cart': cart, 
        'items': items, 
        'product_quantities_in_cart_items': product_quantities_in_cart_items,
        'total_price': total_price
    })

