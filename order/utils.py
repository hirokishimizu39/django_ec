from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.html import strip_tags
import logging
from django.utils.encoding import smart_str
import unicodedata


logger = logging.getLogger(__name__)

def normalize_text(text):
    """テキストを正規化し、エンコーディングの問題を回避する"""
    if not isinstance(text, str):
        return str(text) if text is not None else ''
    
    # NFKC正規化を適用
    text = unicodedata.normalize('NFKC', text)
    
    # 制御文字を削除
    text = ''.join(char for char in text if not unicodedata.category(char).startswith('C'))
    
    return text.strip()

def send_order_confirmation_email(order):
    """注文確認メールを送信する"""
    try:
        # コンテキストデータの正規化
        billing_address = order.billingaddress
        normalized_context = {
            'order': order,
            'billing_address': billing_address,
            'order_items': order.orderitem_set.all(),
        }

        # HTMLメールの作成
        html_message = render_to_string('order/email/order_confirmation.html', normalized_context)
        plain_message = strip_tags(html_message)

        # メールアドレスの正規化
        normalized_email = normalize_text(billing_address.email)
        from_email = f'Django EC Shop <{settings.DEFAULT_FROM_EMAIL}>'

        # デバッグ情報のログ
        logger.debug(f"Normalized plain message: {repr(plain_message)}")
        logger.debug(f"Normalized HTML message: {repr(html_message)}")
        logger.debug(f"From email: {repr(from_email)}")
        logger.debug(f"To email: {repr(normalized_email)}")

        # メール送信
        send_mail(
            subject='[Django EC] Order Confirmation',  # 英語の件名に変更
            message=plain_message,
            from_email=from_email,
            recipient_list=[normalized_email],
            html_message=html_message,
            fail_silently=False
        )
        
        logger.info(f"注文確認メールを送信しました。注文ID: {order.id}")
        
    except Exception as e:
        logger.error(f"注文確認メールの送信に失敗しました。注文ID: {order.id}, エラー: {str(e)}")
        logger.debug(f"Context: {repr(normalized_context)}")
        logger.debug(f"Plain message: {repr(plain_message)}")
        logger.debug(f"HTML message: {repr(html_message)}")
        logger.debug(f"From email: {repr(from_email)}")
        logger.debug(f"To email: {repr(normalized_email)}")