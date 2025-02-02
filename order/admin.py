from django.contrib import admin
from .models import Order, BillingAddress, PaymentInfo, OrderItem
# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display = ('session_id', 'created_at', 'total_price', 'final_price', 'promotion_code', 'is_completed')

admin.site.register(Order, OrderAdmin)


class BillingAddressAdmin(admin.ModelAdmin):
    list_display = ('order', 'first_name', 'last_name', 'user_name', 'email', 'address1', 'address2', 'country', 'city', 'zip_code', 'is_saved_billing_address_info')

admin.site.register(BillingAddress, BillingAddressAdmin)


class PaymentInfoAdmin(admin.ModelAdmin):
    list_display = ('order', 'card_holder_name', 'card_number', 'expiry_date', 'cvv', 'is_saved_payment_info')

admin.site.register(PaymentInfo, PaymentInfoAdmin)


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product_name', 'product_quantity', 'product_price')

admin.site.register(OrderItem, OrderItemAdmin)

