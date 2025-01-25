from django.shortcuts import redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Order, OrderItem
from .forms import BillingAddressForm, PaymentInfoForm
from cart.utils import get_or_create_cart
from django.db import transaction

@require_POST
def purchase(request):
    with transaction.atomic():
        cart = get_or_create_cart(request)
        if not cart or not cart.items.exists():
            messages.warning(request, 'カートが空です。')
            return redirect('cart:cart_view')

        billing_form = BillingAddressForm(request.POST)
        payment_form = PaymentInfoForm(request.POST)

        if billing_form.is_valid() and payment_form.is_valid():
            # 注文の作成
            order = Order.objects.create(
                session_id=request.session.session_key,
                total_price=cart.total_price,
                is_completed=True
            )

            # 請求先住所の保存
            billing_address = billing_form.save(commit=False)
            billing_address.order = order
            billing_address.save()

            # 支払い情報の保存
            payment_info = payment_form.save(commit=False)
            payment_info.order = order
            payment_info.save()

            # カートアイテムを注文アイテムとして保存
            for cart_item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price
                )

            # カートをクリア
            cart.delete()

            # セッションを更新（新しいセッションキーを生成）DBのセッションの一意性は保ちつつ、続けて購入できるようにする
            request.session.cycle_key()
            
            messages.success(request, 'ご購入ありがとうございます。')
            return redirect('shop:product_list')
        else:
            # フォームのエラーメッセージを設定
            for field, errors in billing_form.errors.items():
                for error in errors:
                    messages.error(request, f'{billing_form.fields[field].label}: {error}')
            for field, errors in payment_form.errors.items():
                for error in errors:
                    messages.error(request, f'{payment_form.fields[field].label}: {error}')
            return redirect('cart:cart_saved_info')
