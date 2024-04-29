from django.urls import path
from . import views

urlpatterns = [
    path('search-products/', views.search_products, name='search_products'),
    path('products/<int:product_id>/', views.product_description, name='product_description'),
    path('price_comparison/', views.price_comparison, name='price_comparison'),
]
