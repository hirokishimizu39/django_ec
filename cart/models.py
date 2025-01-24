from django.db import models
from shop.models import Product

# Create your models here.
class Cart(models.Model):
    session_id = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'carts'

    
    def add_item(self, product, quantity=1):
        """カートに商品を1つ追加、または入力された数量分更新"""
        cart_item, created = self.items.get_or_create(cart=self, product=product)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()

    def remove_item(self, product):
        """カートから商品を削除"""
        CartItem.objects.filter(cart=self, product=product).delete()

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = 'cart_items'



