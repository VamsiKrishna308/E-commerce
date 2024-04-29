from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', homepage, name='homepage'),
    path('dashboard/', dashboard, name='dashboard'),
    path('products/', products, name='products'),
    path('categories/', categories, name='categories'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('login1/', login1, name='login1'),
    path('register1/', register1, name='register1'),
    path('logout/', logout, name='logout'),
    path('products/<int:product_id>/', product_description, name='product_description'),
]
