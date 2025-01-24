from .models import Cart, CartItem


def get_or_create_cart(request):
    """セッションごとのカートを取得または作成"""
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key
    
    cart, created = Cart.objects.get_or_create(session_id=session_key)
    return cart

def total_cart_item_quantity(cart):
    cart_items = cart.items.all()
    total_quantity = 0
    for item in cart_items:
        total_quantity += item.quantity
    return total_quantity

def subtotal_cart_item(cart_item):
    return cart_item.product.price * cart_item.quantity

def total_cart_item_price(cart):
    total_price = 0
    for cart_item in cart.items.all():
        total_price += subtotal_cart_item(cart_item)
    return total_price