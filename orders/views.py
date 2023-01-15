from django.shortcuts import render, redirect, get_object_or_404
from .forms import OrderForm
from .models import OrderItem
from cart .models import Cart


def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order, product_variant=item.product_variation, quantity=item.quantity)
            cart.clear()
            return redirect('cart:cart')
    else:
        form = OrderForm()

    context = {
        'form': form,
        'cart': cart
    }
    return render(request, 'orders/checkout.html', context)