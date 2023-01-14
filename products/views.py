from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, VariationOption, VariationValue, ProductVariation, Category
from .forms import ImageFormSet, ProductVariationForm, ProductForm, ImageForm
from django.db import transaction
from django.contrib.auth.decorators import login_required


def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    context = {'products': products, 'categories': categories}
    return render(request, 'products/home.html', context)

def categories(request):
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'products/base.html', context)

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
        form = ProductForm(request.POST, prefix="product")
        image_formset = ImageFormSet(
            request.POST, request.FILES, prefix="images")
        if form.is_valid() and image_formset.is_valid():
            product = form.save(commit=False)
            images = image_formset.save(commit=False)
            images[0].default = True
            try:
                product = Product.objects.get(
                    name=product.name, user=request.user)
            except Product.DoesNotExist:
                product.user = request.user
                product.save()
                for image in images:
                    image.product = product
                    image.save()

            return redirect('products:product_success')
    else:
        form = ProductForm()
        image_formset = ImageFormSet(prefix="images")
    return render(request, 'products/create_product.html', {'form': form, 'image_form': image_formset})


@login_required
@transaction.atomic
def create_product_variation(request):
    if request.method == 'POST':
        form = ProductVariationForm(request.POST)
        image_formset = ImageFormSet(
            request.POST, request.FILES, prefix="images")
        if form.is_valid() and image_formset.is_valid():
            # Create the product variation
            product_variation = form.save(commit=False)
            images = image_formset.save(commit=False)
            try:
                product_variation = ProductVariation.objects.get(
                    name=product_variation.name, user=request.user)
            except ProductVariation.DoesNotExist:
                product_variation.user = request.user
                product_variation.save()
                for image in images:
                    image.variant = product_variation
                    image.save()
            # Redirect to a success page
            return redirect('products:create_variation')
    else:
        form = ProductVariationForm()
        image_formset = ImageFormSet(prefix="images")
    return render(request, 'products/create_variation.html', {'form': form, "image_form": image_formset})


def product_success(request):
    return render(request, "products/products_success.html")
