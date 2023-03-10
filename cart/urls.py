from django.urls import path
from . import views
import settings
from django.conf.urls.static import static


app_name = 'cart'

urlpatterns = [
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:product_id>', views.add_to_cart, name='add_to_cart'),
    path('update_item/<int:item_id>', views.update_cart_item, name='update_item'),
    path('cart/remove/<int:cart_item_id>', views.remove_from_cart, name='remove_from_cart'),

]