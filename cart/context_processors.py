from .utils import get_or_create_cart
from .models import Cart


def cart_quantities(request):
    cart = get_or_create_cart(request)
    if cart:
        total_cart_item = cart.total_quantity
    else:
        total_cart_item = 0
    return {'total_cart_item': total_cart_item}


