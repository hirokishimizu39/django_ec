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
        logger.debug(f"正規化前のテキスト: {repr(text)}")
        
        # 文字列を一度バイト列に変換し、不正な文字を除去
        text = text.encode('utf-8', 'ignore').decode('utf-8')
        logger.debug(f"UTF-8エンコード/デコード後: {repr(text)}")
        
        # NFKC正規化を適用
        text = unicodedata.normalize('NFKC', text)
        logger.debug(f"NFKC正規化後: {repr(text)}")
        
        # 制御文字とサロゲートペアを除去
        text = ''.join(
            char for char in text 
            if not unicodedata.category(char).startswith('C')  # 制御文字を除外
            and not (0xD800 <= ord(char) <= 0xDFFF)  # サロゲートペアを除外
            and ord(char) < 0x10000  # BMP外の文字を除外
        )
        logger.debug(f"文字フィルタリング後: {repr(text)}")
        
        # 空白文字の正規化
        text = ' '.join(text.split())
        logger.debug(f"空白正規化後: {repr(text)}")
        
        result = text.strip()
        logger.debug(f"最終結果: {repr(result)}")
        return result
    except Exception as e:
        logger.error(f"テキスト正規化エラー: {str(e)}, 入力テキスト: {repr(text)}")
        # フォールバック：ASCII文字のみを保持
        return ''.join(c for c in text if ord(c) < 128)

def send_order_confirmation_email(order):
    """注文確認メールを送信する"""
    try:
        # コンテキストデータの正規化
        billing_address = order.billingaddress
        logger.debug(f"元の請求先情報: {repr(billing_address.__dict__)}")
        
        # 各フィールドを個別に正規化
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
            'order_items': []
        }
        
        # 注文アイテムを個別に正規化
        for item in order.orderitem_set.all():
            normalized_item = {
                'product_name': normalize_text(item.product_name),
                'product_quantity': normalize_text(str(item.product_quantity)),
                'product_price': normalize_text(str(item.product_price))
            }
            normalized_context['order_items'].append(normalized_item)
        
        logger.debug(f"正規化後のコンテキスト: {repr(normalized_context)}")

        # HTMLメールの作成
        html_message = render_to_string('order/email/order_confirmation.html', normalized_context)
        plain_message = strip_tags(html_message)

        # メールアドレスの正規化
        normalized_email = normalize_text(billing_address.email)
        from_email = settings.DEFAULT_FROM_EMAIL

        # メール作成前の文字列チェック
        try:
            html_message.encode('utf-8')
            plain_message.encode('utf-8')
        except UnicodeEncodeError as e:
            logger.error(f"メッセージエンコードエラー: {str(e)}")
            logger.debug(f"HTML message: {repr(html_message)}")
            logger.debug(f"Plain message: {repr(plain_message)}")
            raise

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
        logger.debug(f"メール設定:")
        logger.debug(f"- Subject: {repr(email.subject)}")
        logger.debug(f"- From: {repr(from_email)}")
        logger.debug(f"- To: {repr(normalized_email)}")
        logger.debug(f"- Encoding: {email.encoding}")

        # メール送信
        email.send(fail_silently=False)
        logger.info(f"注文確認メールを送信しました。注文ID: {order.id}")
        
    except Exception as e:
        logger.error(f"注文確認メールの送信に失敗しました。注文ID: {order.id}, エラー: {str(e)}")
        logger.error(f"エラーの詳細: {repr(e)}")
        raise