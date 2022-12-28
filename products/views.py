from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, VariationOption, VariationValue, ProductVariation


def home(request):
    featured_products = Product.objects.filter(featured=True)[:6]
    context = {'featured_products': featured_products}
    return render(request, 'products/home.html', context)


def product_list(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'product_list.html', context)


def view_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    variations = ProductVariation.objects.filter(product=product)
    context = {
        'product': product,
        'variations': variations
    }    
    return render(request, 'products/product.html', context)

