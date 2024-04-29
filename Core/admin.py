from django.contrib import admin
from .models import Product, ProductPlatform, Platform

class ProductPlatformInline(admin.TabularInline):
    model = ProductPlatform
    extra = 4  # Allow adding 4 instances of ProductPlatform

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductPlatformInline]

@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    pass
