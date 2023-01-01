from django.forms import ModelForm
from .models import Product, ProductVariation


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "price"]


class ProductVariationForm(ModelForm):
    class Meta:
        model = ProductVariation
        fields = ["name", "product", "option", "value", "price"]