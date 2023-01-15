from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path('', views.home, name='home'),
    path('products/<int:product_id>/', views.view_product, name='view_product'),
    path('products/', views.product_list, name='products'),
    path('create_product/', views.create_product, name='create_product'),
    # path('create_variation/', views.create_product_variation, name='create_variation'),
    path('category_products/<str:category>', views.categories, name='categories'),
     path('user_products/', views.user_products, name='user_products'),
]