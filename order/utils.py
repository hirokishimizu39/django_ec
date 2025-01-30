from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
import logging
import unicodedata
import re


logger = logging.getLogger(__name__)

def normalize_text(text):
    """テキストを正規化し、エンコーディングの問題を回避する"""
    if not isinstance(text, str):
        return str(text) if text is not None else ''
    
    try:
        # NFKC正規化を適用
        text = unicodedata.normalize('NFKC', text)
        
        # サロゲートペアと制御文字を削除
        text = text.encode('utf-8', 'ignore').decode('utf-8')
        
        # 制御文字とNon-BMP文字を削除
        text = ''.join(
            char for char in text 
            if not unicodedata.category(char).startswith('C') 
            and ord(char) < 0x10000
        )
        
        return text.strip()
    except Exception as e:
        logger.error(f"テキスト正規化エラー: {str(e)}, 入力テキスト: {repr(text)}")
        return re.sub(r'[^\x00-\x7F]+', '', text)

def send_order_confirmation_email(order):
    """注文確認メールを送信する"""
    try:
        # コンテキストデータの正規化
        billing_address = order.billingaddress
        normalized_context = {
            'order': {
                'id': normalize_text(str(order.id)),
                'created_at': order.created_at,
                'total_price': normalize_text(str(order.total_price))
            },
            'billing_address': {
                'last_name': normalize_text(billing_address.last_name),
                'first_name': normalize_text(billing_address.first_name),
                'email': normalize_text(billing_address.email),
                'zip_code': normalize_text(billing_address.zip_code),
                'country': normalize_text(billing_address.country),
                'city': normalize_text(billing_address.city),
                'address1': normalize_text(billing_address.address1),
                'address2': normalize_text(billing_address.address2) if billing_address.address2 else ''
            },
            'order_items': [{
                'product_name': normalize_text(item.product_name),
                'product_quantity': normalize_text(str(item.product_quantity)),
                'product_price': normalize_text(str(item.product_price))
            } for item in order.orderitem_set.all()]
        }

        # HTMLメールの作成
        html_message = render_to_string('order/email/order_confirmation.html', normalized_context)
        plain_message = strip_tags(html_message)

        # メールアドレスの正規化
        normalized_email = normalize_text(billing_address.email)
        from_email = settings.DEFAULT_FROM_EMAIL

        # EmailMultiAlternativesを使用してメールを作成
        email = EmailMultiAlternatives(
            subject='[Django EC] Order Confirmation',
            body=plain_message,
            from_email=from_email,
            to=[normalized_email]
        )
        email.attach_alternative(html_message, "text/html")
        email.encoding = 'utf-8'

        # デバッグ情報のログ
        logger.debug(f"Context: {repr(normalized_context)}")
        logger.debug(f"Plain message: {repr(plain_message)}")
        logger.debug(f"HTML message: {repr(html_message)}")
        logger.debug(f"From email: {repr(from_email)}")
        logger.debug(f"To email: {repr(normalized_email)}")

        # メール送信
        email.send(fail_silently=False)
        logger.info(f"注文確認メールを送信しました。注文ID: {order.id}")
        
    except Exception as e:
        logger.error(f"注文確認メールの送信に失敗しました。注文ID: {order.id}, エラー: {str(e)}")
        logger.debug(f"Context: {repr(normalized_context)}")
        logger.debug(f"Plain message: {repr(plain_message)}")
        logger.debug(f"HTML message: {repr(html_message)}")
        logger.debug(f"From email: {repr(from_email)}")
        logger.debug(f"To email: {repr(normalized_email)}")