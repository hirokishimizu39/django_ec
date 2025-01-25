from .models import Cart

def get_or_create_cart(request):
    """セッションごとのカートを取得または作成"""
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key
    
    cart, created = Cart.objects.get_or_create(session_id=session_key)
    return cart