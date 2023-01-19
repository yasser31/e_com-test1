from django.forms import ModelForm
from .models import Product, ProductVariation, Image
from django.forms import formset_factory
from django.forms import inlineformset_factory


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "contact", "price"]


class ProductVariationForm(ModelForm):
    class Meta:
        model = ProductVariation
        fields = ["name", "product", "option", "value", "price"]


class ImageForm(ModelForm):
    class Meta:
        model = Image
        fields = ["image"]


ImageFormSet = inlineformset_factory(
    Product, Image, fields=('image',), extra=4)

