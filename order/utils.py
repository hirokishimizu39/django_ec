from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.html import strip_tags
import logging
from django.utils.encoding import smart_str


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
        logger.debug(f"Plain message: {repr(plain_message)}")
        logger.debug(f"HTML message: {repr(html_message)}")
        logger.debug(f"From email: {repr(from_email)}")
        logger.debug(f"To email: {repr(order.billingaddress.email)}")

        # メール送信
        send_mail(
            subject=smart_str('【ご注文確認】ご注文ありがとうございます', encoding='utf-8', errors='ignore'),
            message=smart_str(plain_message, encoding='utf-8', errors='ignore'),
            from_email=smart_str(from_email, encoding='utf-8', errors='ignore'),
            recipient_list=[smart_str(order.billingaddress.email, encoding='utf-8', errors='ignore')],
            html_message=smart_str(html_message, encoding='utf-8', errors='ignore'),
            fail_silently=False
        )
    except Exception as e:
        # メール送信の失敗は注文処理には影響を与えない
        logger.error(f"注文確認メールの送信に失敗しました。注文ID: {order.id}, エラー: {str(e)}")