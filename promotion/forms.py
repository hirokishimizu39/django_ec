from django import forms
from .models import PromotionCode


class PromotionCodeForm(forms.Form):
    """プロモーションコードフォーム"""
    promotion_code = forms.CharField(
        label='プロモーションコード',
        min_length=7,
        max_length=7,
        error_messages={
            'min_length': 'プロモーションコードは7文字で入力してください',
            'max_length': 'プロモーションコードは7文字で入力してください',
            'required': 'プロモーションコードが入力されていません',
        },
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'プロモーションコード',
        })
    )

    def clean_promotion_code(self):
        """プロモーションコードのバリデーション"""
        input_code = self.cleaned_data['promotion_code']
        try:
            promotion = PromotionCode.objects.get(promotion_code=input_code)
            if promotion.is_used:
                raise forms.ValidationError('このプロモーションコードは既に使用されています')
            return promotion
        except PromotionCode.DoesNotExist:
            raise forms.ValidationError('無効なプロモーションコードです')
        
