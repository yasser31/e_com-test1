from django.forms import ModelForm
from .models import Product, ProductVariation
from django.forms import formset_factory


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "price"]


class ProductVariationForm(ModelForm):
    class Meta:
        model = ProductVariation
        fields = ["name", "product", "option", "value", "price"]



ProductFormSet = formset_factory(ProductForm, extra=4)
ProductVariationFormSet = formset_factory(ProductVariationForm, extra=4)