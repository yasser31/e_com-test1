from django.urls import path
from . import views
from django.conf.urls import handler404, handler500

handler404 = 'orders.views.error_404'
handler500 = 'orders.views.error_500'


app_name = 'orders'

urlpatterns = [
    path('checkout', views.checkout, name="checkout"),
]