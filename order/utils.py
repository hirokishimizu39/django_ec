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
    """Unicodeテキストを安全に処理する関数(Amazon SESによるメール送信の規約に対応する処理)
    
    # 機能概要:
    - 入力テキストのUnicode正規化
    - サロゲートペアの修復
    - 不正な文字の除去
    - 空白文字の正規化
    
    # パラメータ:
    text: 正規化する文字列
    
    # 戻り値:
    正規化されたUnicode文字列
    """
    # 入力が文字列でない場合の処理
    if not isinstance(text, str):
        return str(text) if text is not None else ''

    try:
        # Step 1: バイト列として解釈可能な場合のUTF-8変換処理
        try:
            # 文字列を16進数表現に変換
            hex_str = ''.join(f'{ord(c):04x}' for c in text)
            # UTF-8としてデコード
            byte_str = binascii.unhexlify(hex_str.encode('ascii'))
            text = byte_str.decode('utf-8', errors='ignore')
        except (UnicodeError, binascii.Error):
            # 変換に失敗した場合は元のテキストを使用
            pass

        # Step 2: Unicode正規化（NFKC）の適用
        # NFKCは互換性のある文字を正規化する
        text = unicodedata.normalize('NFKC', text)

        # Step 3: サロゲートペアの修復
        try:
            # UTF-16エンコーディングを使用してサロゲートペアを修復
            text = text.encode('utf-16', 'surrogatepass').decode('utf-16', 'surrogatepass')
        except UnicodeError:
            # サロゲートペアの手動修復処理
            chars = []
            i = 0
            while i < len(text):
                char = text[i]
                # 高位サロゲートの検出
                if 0xD800 <= ord(char) <= 0xDBFF and i + 1 < len(text):
                    next_char = text[i + 1]
                    # 低位サロゲートの検出と組み合わせ
                    if 0xDC00 <= ord(next_char) <= 0xDFFF:
                        chars.append(char + next_char)
                        i += 2
                        continue
                # 通常の文字の処理
                if not (0xD800 <= ord(char) <= 0xDFFF):
                    chars.append(char)
                i += 1
            text = ''.join(chars)

        # Step 4: 問題のある文字の除去
        # - 制御文字
        # - 単独のサロゲート文字
        # - 未割り当ておよびプライベート使用文字
        text = ''.join(
            char for char in text
            if not unicodedata.category(char).startswith('C')
            and not (0xD800 <= ord(char) <= 0xDFFF)
            and unicodedata.category(char) not in {'Co', 'Cn', 'Cs'}
        )

        # Step 5: 空白文字の正規化（連続する空白を単一の空白に）
        text = ' '.join(text.split())

        # Step 6: 最終的なエンコードテスト
        result = text.strip()
        result.encode('utf-8')

        return result

    except Exception as e:
        # エラーログの記録
        logger.error(f"Unicode正規化エラー: {str(e)}, 入力テキスト: {repr(text)}")
        # フォールバック：ASCII文字のみを保持
        return ''.join(c for c in text if ord(c) < 128)

def validate_template_context(context):
    """テンプレートコンテキストの値を再帰的に検証
    
    # 機能:
    - 辞書、リスト、文字列の各要素を正規化
    - ネストされた構造に対応
    
    # パラメータ:
    context: 検証するテンプレートコンテキスト
    
    # 戻り値:
    正規化されたコンテキスト
    """
    if isinstance(context, dict):
        # 辞書の各値を再帰的に処理
        return {k: validate_template_context(v) for k, v in context.items()}
    elif isinstance(context, list):
        # リストの各要素を再帰的に処理
        return [validate_template_context(v) for v in context]
    elif isinstance(context, str):
        # 文字列の場合はUnicode正規化を適用
        try:
            return sanitize_unicode(context)
        except Exception as e:
            logger.error(f"コンテキスト値の正規化エラー: {str(e)}, 値: {repr(context)}")
            return str(context)
    return context

def send_order_confirmation_email(order):
    """注文確認メールを送信する関数
    
    # 機能:
    - 注文情報の正規化
    - HTMLとプレーンテキストメールの生成
    - メールの送信
    
    # パラメータ:
    order: 注文オブジェクト
    
    # 例外:
    メール送信失敗時に例外を発生
    """
    try:
        # 請求先情報の取得とデバッグログ
        billing_address = order.billingaddress
        logger.debug(f"元の請求先情報: {repr(billing_address.__dict__)}")
        
        # メールテンプレート用のコンテキスト作成
        # 全てのフィールドでUnicode正規化を適用
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

        # HTMLメールの生成と正規化
        html_message = render_to_string('order/email/order_confirmation.html', context)
        html_message = sanitize_unicode(html_message)
        
        # HTMLからプレーンテキストを生成
        plain_message = strip_tags(html_message)
        plain_message = sanitize_unicode(plain_message)

        # メールアドレスの正規化
        normalized_email = sanitize_unicode(billing_address.email)
        from_email = settings.DEFAULT_FROM_EMAIL

        # マルチパートメールの作成
        email = EmailMultiAlternatives(
            subject='[Django EC] Order Confirmation',
            body=plain_message,
            from_email=from_email,
            to=[normalized_email]
        )
        
        # HTMLバージョンの添付
        email.attach_alternative(html_message, "text/html")
        email.encoding = 'utf-8'

        # デバッグ情報のログ記録
        logger.debug(f"メール設定:")
        logger.debug(f"- Subject: {repr(email.subject)}")
        logger.debug(f"- From: {repr(from_email)}")
        logger.debug(f"- To: {repr(normalized_email)}")
        logger.debug(f"- Body: {repr(plain_message)}")
        logger.debug(f"- HTML: {repr(html_message)}")

        # メール送信（エラーを伝播）
        email.send(fail_silently=False)
        logger.info(f"注文確認メールを送信しました。注文ID: {order.id}")
        
    except Exception as e:
        # エラーログの記録と例外の再発生
        logger.error(f"注文確認メールの送信に失敗しました。注文ID: {order.id}, エラー: {str(e)}")
        logger.error(f"エラーの詳細: {repr(e)}")
        raise