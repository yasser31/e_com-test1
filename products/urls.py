from e__com import settings
from django.urls import path
from . import views
from django.conf.urls.static import static

app_name = "products"

urlpatterns = [
    path('', views.home, name='home'),
    path('products/<int:product_id>/', views.view_product, name='view_product'),
    path('products/', views.product_list, name='products'),
    path('create_product/', views.create_product, name='create_product'),
    path('create_variation/', views.create_product_variation, name='create_variation'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)