from django.shortcuts import render, redirect, get_object_or_404
from .utils import get_or_create_cart, remove_from_cart, total_cart_item_price, total_cart_item_quantity
from shop.models import Product


def add_to_cart_view(request, product_id):
    """商品をカートに追加するビュー"""
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    cart = get_or_create_cart(request)
    cart.add_item(product, quantity)
    
    # カートに入れる押下時、一覧画面からなら一覧画面に、詳細画面からなら詳細画面にリダイレクト
    # Refererヘッダーは信頼性が低いため、ない場合は無条件で一覧画面へリダイレクト
    referer_url = request.META.get('HTTP_REFERER')
    return redirect(referer_url if referer_url else 'shop:product_list')

def remove_from_cart_view(request, product_id):
    """カートから商品を削除するビュー"""
    product = get_object_or_404(Product, id=product_id)
    remove_from_cart(request, product)
    return redirect('cart:cart_view')

def cart_view(request):
    """カートの中身を表示するビュー"""
    cart = get_or_create_cart(request)
    items = cart.items.select_related('product')
    total_cart_item = total_cart_item_quantity(cart)
    total_price = total_cart_item_price(cart)
    return render(request, 'cart/cart.html', {
        'cart': cart, 
        'items': items, 
        'total_cart_item': total_cart_item,
        'total_price': total_price
    })

