from django import forms
from .models import BillingAddress, PaymentInfo

class BillingAddressForm(forms.ModelForm):
    class Meta:
        model = BillingAddress
        fields = [
            'first_name', 'last_name', 'user_name', 'email',
            'address1', 'address2', 'country', 'city', 'zip_code',
            'is_saved_billing_address_info'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'user_name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address1': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'address2': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'is_saved_billing_address_info': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }

class PaymentInfoForm(forms.ModelForm):
    class Meta:
        model = PaymentInfo
        fields = [
            'card_holder_name', 'card_number', 'expiry_date',
            'cvv', 'is_saved_payment_info'
        ]
        widgets = {
            'card_holder_name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'card_number': forms.TextInput(attrs={
                'class': 'form-control',
                'required': True,
                'pattern': '[0-9]{16}',
                'title': '16桁の数字を入力してください'
            }),
            'expiry_date': forms.TextInput(attrs={
                'class': 'form-control',
                'required': True,
                'pattern': '[0-9]{2}/[0-9]{2}',
                'placeholder': 'MM/YY',
                'title': 'MM/YY形式で入力してください'
            }),
            'cvv': forms.TextInput(attrs={
                'class': 'form-control',
                'required': True,
                'pattern': '[0-9]{3,4}',
                'title': '3桁または4桁の数字を入力してください'
            }),
            'is_saved_payment_info': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
