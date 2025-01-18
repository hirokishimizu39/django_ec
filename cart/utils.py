from .models import Cart, CartItem

def get_or_create_cart(request):
    """セッションごとのカートを取得または作成"""
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key
    
    cart, created = Cart.objects.get_or_create(session_id=session_key)
    return cart


def add_to_cart(request, product, quantity=1):
    """カートに商品を1つ追加、または入力された数量分更新"""
    cart = get_or_create_cart(request)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    cart_item.save()


def remove_from_cart(request, product):
    cart = get_or_create_cart(request)
    CartItem.objects.filter(cart=cart, product=product).delete()

    