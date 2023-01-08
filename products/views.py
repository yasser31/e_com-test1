from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, VariationOption, VariationValue, ProductVariation
from .forms import ProductForm, ProductVariationFormSet
from django.db import transaction
from django.contrib.auth.decorators import login_required


def home(request):
    products = Product.objects.all()
    context = {'products': products}
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



@login_required
@transaction.atomic
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            return redirect('products:product_success')
    else:
        form = ProductForm()
    return render(request, 'products/create_product.html', {'form': form})


@login_required
@transaction.atomic
def create_product_variation(request):
    if request.method == 'POST':
        formset = ProductVariationFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
            # Create the product variation
                product_variation = form.save()
            # Redirect to a success page
            return redirect('products:view_product', product_variation.product.pk)
    else:
        form = ProductVariationFormSet()
    return render(request, 'products/create_variation.html', {'form': form})


def product_success(request):
    return render(request, "products/product_success.html")