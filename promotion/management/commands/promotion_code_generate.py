from django.core.management.base import BaseCommand
from promotion.models import PromotionCode

# プロモーションコード生成用のカスタムコマンド
class Command(BaseCommand):
    help = 'プロモーションコードをランダムに10個生成します'

    def handle(self, *args, **options):
        created_promotion_codes = []

        for _ in range(10):
            random_code = PromotionCode.generate_code()
            random_discount_amount = PromotionCode.generate_discount_amount()
            
            promotion_code = PromotionCode.objects.create(
                promotion_code=random_code,
                discount_amount=random_discount_amount
            )
            created_promotion_codes.append(promotion_code)
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'プロモーションコード "{random_code}" を作成しました(割引額: ¥{random_discount_amount})'
                )
            )
        
        self.stdout.write(
            self.style.SUCCESS(f'合計{len(created_promotion_codes)}個のプロモーションコードを生成しました')
        ) 