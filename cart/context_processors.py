from .utils import get_or_create_cart
from django.db.models import Sum

def cart_quantities(request):
    cart = get_or_create_cart(request)
    if cart:
        total_product_quantities_in_cart_items = cart.items.aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0
    else:
        total_product_quantities_in_cart_items = 0
    return {'total_product_quantities_in_cart_items': total_product_quantities_in_cart_items}