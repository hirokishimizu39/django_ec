from django.db import models
from shop.models import Product

# Create your models here.
class Order(models.Model):
    session_id = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.id} for session {self.session_id}"


class BillingAddress(models.Model):
    order = models.OneToOneField('Order', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    user_name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    is_saved_billing_address_info = models.BooleanField(default=False)

    def __str__(self):
        return f"BillingAddress {self.id} for order {self.order.id}"


class PaymentInfo(models.Model):
    order = models.OneToOneField('Order', on_delete=models.CASCADE)
    card_holder_name = models.CharField(max_length=255)
    card_number = models.CharField(max_length=16)
    expiry_date = models.CharField(max_length=5)
    cvv = models.CharField(max_length=4)
    is_saved_payment_info = models.BooleanField(default=False)

    def __str__(self):
        return f"PaymentInfo {self.id} for order {self.order.id}"


class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255, null=True, blank=True)
    product_quantity = models.IntegerField(null=True, blank=True)
    product_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"OrderItem {self.id} for order {self.order.id}"


