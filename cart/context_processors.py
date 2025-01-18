from .utils import get_or_create_cart, total_cart_item_quantity


def cart_quantities(request):
    cart = get_or_create_cart(request)
    if cart:
        total_cart_item = total_cart_item_quantity(cart)
    else:
        total_cart_item = 0
    return {'total_cart_item': total_cart_item}


