from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import random
import string

class PromotionCode(models.Model):
    """プロモーションコードモデル"""
    promotion_code = models.CharField(max_length=7, unique=True, verbose_name='プロモーションコード')
    discount_amount = models.DecimalField(max_digits=5, decimal_places=0, validators=[MinValueValidator(100), MaxValueValidator(1000)], verbose_name='割引額')
    is_used = models.BooleanField(default=False, verbose_name='プロモーションコード使用済みフラグ')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='プロモーションコード作成日時')
    used_at = models.DateTimeField(null=True, blank=True, verbose_name='プロモーションコード使用日時')

    class Meta:
        db_table = 'promotion_code'
        indexes = [
            models.Index(fields=['promotion_code']),
            models.Index(fields=['is_used']),
        ]

    def __str__(self):
        return f'{self.promotion_code} (¥{self.discount_amount})'


    @staticmethod
    def generate_code():
        """7桁のランダムな英数字コードを生成"""
        while True:
            # 英大文字と数字を使用して7桁のコードを生成
            promotion_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
            # コードの重複チェック
            if not PromotionCode.objects.filter(promotion_code=promotion_code).exists():
                return promotion_code
    
    @staticmethod
    def generate_discount_amount():
        """100~1000円の間でランダムな割引額を生成"""
        return random.randint(100, 1000)
    
