# urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Other paths
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('view-cart/', views.view_cart, name='view_cart'),
    path('delete-cart-item/<int:cart_item_id>/', views.delete_cart_item, name='delete_cart_item'),
]
