from django.shortcuts import render, redirect, get_object_or_404
from .models import CartItem, Cart
from products.models import ProductVariation
from django.http import JsonResponse


def cart(request):
    items = CartItem.objects.filter(user=request.user)
    cart = Cart.objects.get(user=request.user)
    context = {'items': items, 'cart': cart}
    return render(request, 'cart/cart.html', context)


def add_to_cart(request, product_id):
    if request.method == "POST":
        # Get the current user's cart
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=request.user)

        # Get the product variation IDs from the form submission
        product_variation_ids = request.POST.getlist('product_variations')

        # Create a CartItem for each product variation
        for variation_id in product_variation_ids:
            variation = ProductVariation.objects.get(pk=variation_id)
            try:
                item = CartItem.objects.get(
                    product_variation=variation, user=request.user)
            except CartItem.DoesNotExist:
                item = CartItem.objects.create(
                    cart=cart, product_variation=variation, quantity=1, user=request.user)
        # Redirect the user back to the product page
        return redirect('view_product', product_id=product_id)
    return redirect('view_product', product_id=product_id)


def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, pk=cart_item_id)
    cart_item.delete()
    return redirect('cart:cart')

def update_cart_item(request):
    if request.method == 'POST':
        item_id = request.POST['item_id']
        new_quantity = request.POST['quantity']
        cart_item = get_object_or_404(CartItem, pk=item_id)
        cart_item.update_quantity(new_quantity)
        cart = cart_item.cart
        cart.update_total_price()
        data = {
            'new_total_price': cart_item.price,
            'new_cart_total': cart.total_price,
        }
        return JsonResponse(data)