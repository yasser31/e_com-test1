from django.contrib import admin
from .models import Product, VariationOption, VariationValue, ProductVariation

admin.site.register(Product)
admin.site.register(VariationOption)
admin.site.register(VariationValue)
admin.site.register(ProductVariation)