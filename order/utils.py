from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
import logging
import unicodedata
import re


logger = logging.getLogger(__name__)

def fix_surrogates(text):
    """サロゲートペアを修復または除去する"""
    try:
        # サロゲートペアを含む文字列をバイト列として解釈
        return text.encode('utf-16', 'surrogatepass').decode('utf-16')
    except UnicodeError:
        # 修復できない場合は、サロゲートペアを除去
        return ''.join(c for c in text if not (0xD800 <= ord(c) <= 0xDFFF))

def normalize_text(text):
    """テキストを正規化し、エンコーディングの問題を回避する"""
    if not isinstance(text, str):
        return str(text) if text is not None else ''
    
    try:
        logger.debug(f"正規化前のテキスト: {repr(text)}")
        
        # サロゲートペアの修復
        text = fix_surrogates(text)
        logger.debug(f"サロゲートペア修復後: {repr(text)}")
        
        # NFKC正規化を適用（合成文字を分解し、互換文字を正規化）
        text = unicodedata.normalize('NFKC', text)
        logger.debug(f"NFKC正規化後: {repr(text)}")
        
        # 制御文字を除去し、表示可能な文字のみを保持
        text = ''.join(
            char for char in text 
            if not unicodedata.category(char).startswith('C')  # 制御文字を除外
            and unicodedata.category(char) not in {'Co', 'Cn'}  # 未割り当ておよびプライベート利用文字を除外
        )
        logger.debug(f"文字フィルタリング後: {repr(text)}")
        
        # 空白文字の正規化（連続する空白を単一の空白に）
        text = ' '.join(text.split())
        logger.debug(f"空白正規化後: {repr(text)}")
        
        # 最終的なUTF-8エンコードテスト
        result = text.strip()
        result.encode('utf-8')  # エンコードテスト
        
        logger.debug(f"最終結果: {repr(result)}")
        return result
    except Exception as e:
        logger.error(f"テキスト正規化エラー: {str(e)}, 入力テキスト: {repr(text)}")
        # フォールバック：安全な文字のみを保持
        return ''.join(c for c in text if ord(c) < 128)

def validate_template_context(context):
    """テンプレートコンテキストの各値を検証"""
    if isinstance(context, dict):
        return {k: validate_template_context(v) for k, v in context.items()}
    elif isinstance(context, list):
        return [validate_template_context(v) for v in context]
    elif isinstance(context, str):
        try:
            return normalize_text(context)
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
        
        # 基本コンテキストの作成
        context = {
            'order': {
                'id': str(order.id),
                'created_at': order.created_at,
                'total_price': str(order.total_price)
            },
            'billing_address': {
                'last_name': billing_address.last_name,
                'first_name': billing_address.first_name,
                'email': billing_address.email,
                'zip_code': billing_address.zip_code,
                'country': billing_address.country,
                'city': billing_address.city,
                'address1': billing_address.address1,
                'address2': billing_address.address2 if billing_address.address2 else ''
            },
            'order_items': [{
                'product_name': item.product_name,
                'product_quantity': str(item.product_quantity),
                'product_price': str(item.product_price)
            } for item in order.orderitem_set.all()]
        }
        
        # コンテキスト全体を正規化
        normalized_context = validate_template_context(context)
        logger.debug(f"正規化後のコンテキスト: {repr(normalized_context)}")

        # HTMLメールの作成とエンコードテスト
        html_message = render_to_string('order/email/order_confirmation.html', normalized_context)
        try:
            html_message.encode('utf-8')
        except UnicodeEncodeError as e:
            logger.error(f"HTMLメッセージのエンコードエラー: {str(e)}")
            html_message = normalize_text(html_message)
        
        # プレーンテキストの作成とエンコードテスト
        plain_message = strip_tags(html_message)
        try:
            plain_message.encode('utf-8')
        except UnicodeEncodeError as e:
            logger.error(f"プレーンテキストのエンコードエラー: {str(e)}")
            plain_message = normalize_text(plain_message)

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