from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, VariationOption, VariationValue, ProductVariation, Category, Image
from .forms import ImageFormSet, ProductVariationForm, ProductForm
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DeleteView
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Q
from django.db.models import F
from django.http import JsonResponse
from .functions import products_to_dict
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import json
import sentry_sdk


def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    context = {'products': products, 'categories': categories}
    if not products:
        messages.warning(
            request, "Aucun produit pour le moment, vous pouvez en ajouter en haut à droite")
    return render(request, 'products/home.html', context)


def categories(request, category):
    category_products = Product.objects.filter(
        category__name=category).order_by('-created_date')
    context = {
        'products': category_products,
    }
    if not category_products:
        messages.warning(
            request, "Aucun produit dans cette catégorie pour le moment, vous pouvez en ajouter un produit en haut à droite")
    return render(request, 'products/category.html', context)


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
        image_formset = ImageFormSet(
            request.POST, request.FILES, prefix="images")
        if form.is_valid() and image_formset.is_valid():
            product = form.save(commit=False)
            images = image_formset.save(commit=False)
            try:
                product = Product.objects.get(
                    name=product.name, user=request.user)
            except Product.DoesNotExist:
                product.user = request.user
                product.save()
                for image in images:
                    image.product = product
                    image.save()
            messages.success(
                request, "Votre produit a été crée avec succès veuillez en ajouter un autre")
            return redirect('products:create_product')
    else:
        form = ProductForm()
        image_formset = ImageFormSet(prefix="images")
    messages.warning(request, "Veuillez choisir une seule image principale")
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


def user_products(request):
    products = Product.objects.filter(
        user=request.user).order_by("-created_date")
    if not products:
        messages.warning(
            request, "Vous n'avez aucun produit vous pouvez en ajouter en haut à droite")
    context = {
        "products": products
    }
    return render(request, "products/user_products.html", context)


class ProductEditView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_edit.html'
    success_url = reverse_lazy('products:create_product')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        image_formset = ImageFormSet()
        return self.render_to_response(
            self.get_context_data(form=form, image_form=image_formset)
        )

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        image_formset = ImageFormSet(
            self.request.POST, self.request.FILES, instance=self.object)
        if form.is_valid() and image_formset.is_valid():
            return self.form_valid(form, image_formset)
        else:
            return self.form_invalid(form, image_formset)

    def form_valid(self, form, image_formset):
        self.object = form.save()
        image_formset.instance = self.object
        image_formset.save()
        messages.success(self.request, "Produit modifié avec succès")
        return redirect(self.get_success_url())

    def form_invalid(self, form, image_formset):
        return self.render_to_response(
            self.get_context_data(form=form, image_form=image_formset)
        )


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'products/product_confirm_delete.html'
    success_url = reverse_lazy('products:home')

    def delete(self, request, *args, **kwargs):
        """
        Override the delete method to delete related images as well.
        """
        self.object = self.get_object()
        self.object.delete()
        messages.warning(request, "Produit supprimé !")
        return redirect(self.get_success_url())


class ImageDeleteView(DeleteView):
    model = Image
    template_name = 'products/image_confirm_delete.html'
    success_url = reverse_lazy('products:home')

    def delete(self, request, *args, **kwargs):
        """
        Override the delete method to delete related images as well.
        """
        self.object = self.get_object()
        self.object.delete()
        messages.warning(request, "Image supprimé!")
        return redirect(self.get_success_url())


def search(request, query):
    products = Product.objects.filter(
        Q(name__icontains=query) |
        Q(category__name__icontains=query) |
        Q(description__icontains=query)
    )
    filtered_products = products_to_dict(products)
    return JsonResponse({'products': filtered_products})


@csrf_exempt
def filter_home(request):
    data = json.load(request)
    categories = data["categories"]
    price_type = data["price"]
    products = None
    if categories and price_type:
        if price_type[0] == "increasing":
            products = Product.objects.filter(
                category__name__in=categories).order_by("price")
        elif price_type[0] == "decreasing":
            products = Product.objects.filter(
                category__name__in=categories).order_by("-price")
    elif price_type and not categories:
        if price_type[0] == "increasing":
            products = Product.objects.all().order_by("price")
        elif price_type[0] == "decreasing":
            products = Product.objects.all().order_by("-price")
    elif categories and not price_type:
        products = Product.objects.filter(category__name__in=categories)
    else:
        products = Product.objects.all()

    filtered_products = products_to_dict(products)
    return JsonResponse({'products': filtered_products})
