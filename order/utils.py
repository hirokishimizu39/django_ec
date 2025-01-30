from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
import logging
import unicodedata
import re
import binascii


logger = logging.getLogger(__name__)

def sanitize_unicode(text):
    """Unicodeテキストを安全に処理する包括的な関数"""
    if not isinstance(text, str):
        return str(text) if text is not None else ''

    try:
        # Step 1: バイト列として解釈可能な場合、正しいUTF-8に変換
        try:
            # 16進数表現に変換して解析
            hex_str = ''.join(f'{ord(c):04x}' for c in text)
            # UTF-8としてデコード
            byte_str = binascii.unhexlify(hex_str.encode('ascii'))
            text = byte_str.decode('utf-8', errors='ignore')
        except (UnicodeError, binascii.Error):
            pass

        # Step 2: NFKC正規化を適用
        text = unicodedata.normalize('NFKC', text)

        # Step 3: サロゲートペアの修復試行
        try:
            text = text.encode('utf-16', 'surrogatepass').decode('utf-16', 'surrogatepass')
        except UnicodeError:
            # サロゲートペアの修復に失敗した場合、個別に処理
            chars = []
            i = 0
            while i < len(text):
                char = text[i]
                if 0xD800 <= ord(char) <= 0xDBFF and i + 1 < len(text):
                    # 正しいサロゲートペアの場合
                    next_char = text[i + 1]
                    if 0xDC00 <= ord(next_char) <= 0xDFFF:
                        chars.append(char + next_char)
                        i += 2
                        continue
                if not (0xD800 <= ord(char) <= 0xDFFF):
                    # 通常の文字の場合
                    chars.append(char)
                i += 1
            text = ''.join(chars)

        # Step 4: 制御文字と問題のある文字を除去
        text = ''.join(
            char for char in text
            if not unicodedata.category(char).startswith('C')  # 制御文字を除外
            and not (0xD800 <= ord(char) <= 0xDFFF)  # サロゲートを除外
            and unicodedata.category(char) not in {'Co', 'Cn', 'Cs'}  # 未割り当ておよびサロゲート文字を除外
        )

        # Step 5: 空白文字の正規化
        text = ' '.join(text.split())

        # Step 6: 最終エンコードテスト
        result = text.strip()
        result.encode('utf-8')

        return result

    except Exception as e:
        logger.error(f"Unicode正規化エラー: {str(e)}, 入力テキスト: {repr(text)}")
        # 最終的なフォールバック：ASCII文字のみを保持
        return ''.join(c for c in text if ord(c) < 128)

def validate_template_context(context):
    """テンプレートコンテキストの各値を検証"""
    if isinstance(context, dict):
        return {k: validate_template_context(v) for k, v in context.items()}
    elif isinstance(context, list):
        return [validate_template_context(v) for v in context]
    elif isinstance(context, str):
        try:
            return sanitize_unicode(context)
        except Exception as e:
            logger.error(f"コンテキスト値の正規化エラー: {str(e)}, 値: {repr(context)}")
            return str(context)
    return context

def send_order_confirmation_email(order):
    """注文確認メールを送信する"""
    try:
        # コンテキストデータの正規化
        billing_address = order.billingaddress
        logger.debug(f"元の請求先情報: {repr(billing_address.__dict__)}")
        
        # 基本コンテキストの作成と正規化
        context = {
            'order': {
                'id': sanitize_unicode(str(order.id)),
                'created_at': order.created_at,
                'total_price': sanitize_unicode(str(order.total_price))
            },
            'billing_address': {
                'last_name': sanitize_unicode(billing_address.last_name),
                'first_name': sanitize_unicode(billing_address.first_name),
                'email': sanitize_unicode(billing_address.email),
                'zip_code': sanitize_unicode(billing_address.zip_code),
                'country': sanitize_unicode(billing_address.country),
                'city': sanitize_unicode(billing_address.city),
                'address1': sanitize_unicode(billing_address.address1),
                'address2': sanitize_unicode(billing_address.address2) if billing_address.address2 else ''
            },
            'order_items': [{
                'product_name': sanitize_unicode(item.product_name),
                'product_quantity': sanitize_unicode(str(item.product_quantity)),
                'product_price': sanitize_unicode(str(item.product_price))
            } for item in order.orderitem_set.all()]
        }

        logger.debug(f"正規化後のコンテキスト: {repr(context)}")

        # HTMLメールの作成
        html_message = render_to_string('order/email/order_confirmation.html', context)
        html_message = sanitize_unicode(html_message)
        
        # プレーンテキストの作成
        plain_message = strip_tags(html_message)
        plain_message = sanitize_unicode(plain_message)

        # メールアドレスの正規化
        normalized_email = sanitize_unicode(billing_address.email)
        from_email = settings.DEFAULT_FROM_EMAIL

        # EmailMultiAlternativesを使用してメール作成
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
        logger.debug(f"- Body: {repr(plain_message)}")
        logger.debug(f"- HTML: {repr(html_message)}")

        # メール送信
        email.send(fail_silently=False)
        logger.info(f"注文確認メールを送信しました。注文ID: {order.id}")
        
    except Exception as e:
        logger.error(f"注文確認メールの送信に失敗しました。注文ID: {order.id}, エラー: {str(e)}")
        logger.error(f"エラーの詳細: {repr(e)}")
        raise