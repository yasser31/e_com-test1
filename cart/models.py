from django.db import models
from products.models import Product
from django.contrib.auth.models import User
from products.models import ProductVariation 

class Cart(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_variation = models.ManyToManyField(ProductVariation)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    def __str__(self):
        return f'{self.user} cart'
    
    def update_total_price(self):
        total_price = 0
        for item in self.items.all():
            total_price += item.total
        self.total = total_price
        self.save()
        print("price_updated")
    
    def clear(self):
        cart_items = CartItem.objects.filter(cart=self)
        cart_items.delete()


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    product_variation = models.ForeignKey(ProductVariation, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    total = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    def update_quantity(self, new_quantity):
        self.quantity = new_quantity
        if self.product_variation:
            self.total = self.product_variation.price * new_quantity
        elif self.product:
            self.total = self.product.price * new_quantity
        self.save()
        print("quantity_updated")
