from django.urls import path
from . import views
from e__com import settings
from django.conf.urls.static import static
from django.conf.urls import handler404, handler500

handler404 = 'cart.views.error_404'
handler500 = 'cart.views.error_500'


app_name = 'cart'

urlpatterns = [
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:product_id>', views.add_to_cart, name='add_to_cart'),
    path('update_item/<int:item_id>', views.update_cart_item, name='update_item'),
    path('cart/remove/<int:cart_item_id>', views.remove_from_cart, name='remove_from_cart'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)