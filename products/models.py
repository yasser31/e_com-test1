from django.db import models
from PIL import Image


class VariationOption(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class VariationValue(models.Model):
    option = models.ForeignKey(VariationOption, on_delete=models.CASCADE)
    value = models.CharField(max_length=100)
    dependency = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey('Product', on_delete=models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return self.value

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='products/static/products/img')
    variations = models.ManyToManyField(VariationOption)

    def __str__(self):
        return self.name


class ProductVariation(models.Model):

    name = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    option = models.ManyToManyField(VariationOption, blank=True)
    value = models.ManyToManyField(VariationValue, blank=True)

    def __str__(self):
        return self.name 