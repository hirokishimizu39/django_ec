from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.html import strip_tags
import logging

logger = logging.getLogger(__name__)

def send_order_confirmation_email(order):
    """注文確認メールを送信する"""
    try:
        context = {
            'order': order,
            'billing_address': order.billingaddress,
            'order_items': order.orderitem_set.all(),
        }

        # HTMLメールの作成
        html_message = render_to_string('order/email/order_confirmation.html', context)
        # htmlタグを削除
        plain_message = strip_tags(html_message)

        # 送信者名を設定（例：Django EC Shop <no-reply@example.com>）
        from_email = f'Django EC Shop <{settings.DEFAULT_FROM_EMAIL}>'

        # メール送信
        send_mail(
            subject='【ご注文確認】ご注文ありがとうございます',
            message=plain_message,
            from_email=from_email,
            recipient_list=[order.billingaddress.email],
            html_message=html_message,
            fail_silently=False
        )
    except Exception as e:
        # メール送信の失敗は注文処理には影響を与えない
        logger.error(f"注文確認メールの送信に失敗しました。注文ID: {order.id}, エラー: {str(e)}")