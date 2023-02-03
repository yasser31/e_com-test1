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
    path('edit_products/<int:pk>', views.ProductEditView.as_view(), name='edit_product'),
    path('delete_product/<int:pk>/', views.ProductDeleteView.as_view(), name='product_delete'),
    path('delete_image/<int:pk>/', views.ImageDeleteView.as_view(), name='image_delete'),
    path('search/', views.search, name='search'),
    path('products/filter_home', views.filter_home, name='filter_home'),
]