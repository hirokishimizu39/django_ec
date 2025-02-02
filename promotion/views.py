from django.views.generic import View
from promotion.forms import PromotionCodeForm
from promotion.models import PromotionCode
from django.shortcuts import redirect, render
from django.contrib import messages
from cart.utils import get_or_create_cart
from django.views.decorators.http import require_POST
from django.utils import timezone

@require_POST
def apply_promotion_code(request):
    """プロモーションコードを適用する"""
    cart = get_or_create_cart(request)
    if not cart.items.exists():
        messages.warning(request, 'カートが空です。商品を追加してから、プロモーションコードを適用してください。')
        return redirect('cart:cart_view')

    form = PromotionCodeForm(request.POST)
    if not form.is_valid():
        messages.error(request, form.errors['promotion_code'][0])
        return redirect('cart:cart_view')

    promotion = form.cleaned_data['promotion_code']
    request.session['promotion_code'] = {
        'id': promotion.id,
        'promotion_code': promotion.promotion_code,
        'discount_amount': float(promotion.discount_amount),
    }

    total_price_with_discount = max(0, cart.total_price - promotion.discount_amount)
    context = {
        'cart': cart,
        'items': cart.items.select_related('product'),
        'total_cart_item': cart.total_quantity,
        'total_price': cart.total_price,
        'total_price_with_discount': total_price_with_discount,
        'promotion_code': promotion.promotion_code,
        'discount_amount': promotion.discount_amount,
    }

    messages.success(
        request,
        f'プロモーションコード "{promotion.promotion_code}" を適用しました(割引額: ¥{promotion.discount_amount:,})'
    )
    return render(request, 'cart/cart.html', context)


@require_POST
def remove_promotion_code(request):
    """プロモーションコードを削除する"""
    if 'promotion_code' in request.session:
        del request.session['promotion_code']
        messages.success(request, 'プロモーションコードを削除しました')
    return redirect('cart:cart_view')


def process_promotion_code(request, total_price):
    """プロモーションコードを適用する"""
    promotion = None
    total_price_with_discount = total_price
    if 'promotion_code' in request.session:
        try:
            promotion_data = request.session['promotion_code']
            promotion = PromotionCode.objects.get(id=promotion_data['id'])
            if promotion.is_used:
                return None, total_price
            promotion.is_used = True
            promotion.used_at = timezone.now()
            promotion.save()
            
            total_price_with_discount = max(0, total_price - promotion.discount_amount)
        except PromotionCode.DoesNotExist:
            messages.warning(request, 'プロモーションコードの適用に失敗しました。')
    return promotion, total_price_with_discount