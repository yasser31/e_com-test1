from django.shortcuts import render, redirect, get_object_or_404
from .models import CartItem, Cart
from products.models import ProductVariation, Product
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json


def cart(request):
    items = CartItem.objects.filter(user=request.user)
    cart = Cart.objects.get(user=request.user)
    context = {'items': items, 'cart': cart}
    return render(request, 'cart/cart.html', context)


@login_required
def add_to_cart(request, product_id):
    if request.method == "POST":
        # Get the current user's cart
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=request.user)
        '''
        # Get the product variation IDs from the form submission
        if product_variation_ids:
            # Create a CartItem for each product variation
            for variation_id in product_variation_ids:
                variation = ProductVariation.objects.get(pk=variation_id)
                try:
                    item = CartItem.objects.get(
                    product_variation=variation, user=request.user)
                except CartItem.DoesNotExist:
                    item = CartItem.objects.create(
                        cart=cart, product_variation=variation, quantity=1, user=request.user)
                    item.total = item.product_variation.price * item.quantity
                    cart.total += item.total
                    cart.save()
                    item.save()
        '''
        product = Product.objects.get(pk=product_id)
        try:
            item = CartItem.objects.get(
            product=product, user=request.user)
        except CartItem.DoesNotExist:
            item = CartItem.objects.create(
                cart=cart, product=product, quantity=1, user=request.user)
            item.total = item.product.price * item.quantity
            cart.total += item.total
            cart.save()
            item.save()
            

        # Redirect the user back to the product page
        return redirect('products:view_product', product_id=product_id)
    return redirect('products:view_product', product_id=product_id)


def remove_from_cart(request, cart_item_id):
    if request.method == "POST":
        cart_item = get_object_or_404(CartItem, pk=cart_item_id)
        cart = cart_item.cart
        new_cart_total = cart.total - cart_item.total
        cart.total = new_cart_total
        cart.save()
        cart_item.delete()
        data = {
            'new_cart_total': new_cart_total
        }
        return JsonResponse(data)

def update_cart_item(request, item_id):
    if request.method == 'POST':
        new_quantity = json.load(request)["quantity"]
        cart_item = get_object_or_404(CartItem, pk=item_id)
        cart_item.update_quantity(int(new_quantity))
        cart = cart_item.cart
        cart.update_total_price()
        data = {
            'new_item_total': cart_item.total,
            'new_cart_total': cart.total,
        }
        return JsonResponse(data)