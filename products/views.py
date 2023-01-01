from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, VariationOption, VariationValue, ProductVariation
from .forms import ProductForm, ProductVariationForm
from django.db import transaction



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


@transaction.atomic
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            return redirect('products:view_product', product.pk)
    else:
        form = ProductForm()
    return render(request, 'products/create_product.html', {'form': form})



@transaction.atomic
def create_product_variation(request):
    if request.method == 'POST':
        form = ProductVariationForm(request.POST)
        if form.is_valid():
            # Create the product variation
            product_variation = form.save()
            # Redirect to a success page
            return redirect('products:view_product')
    else:
        form = ProductVariationForm()
    return render(request, 'products/create_variation.html', {'form': form})
