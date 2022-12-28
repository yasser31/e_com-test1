from django.db import models
from products.models import Product, ProductVariation


class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(null=True, blank=True)
    address = models.CharField(max_length=250, null=True, blank=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Order {}'.format(self.id)


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name='items', on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(
        Product, related_name='order_items', on_delete=models.CASCADE, null=True, blank=True)
    product_variant = models.ForeignKey(
        ProductVariation, related_name='order_variants', on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1, null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
