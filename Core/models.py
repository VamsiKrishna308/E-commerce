from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    features = models.TextField()
    image = models.ImageField(upload_to='static/product_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    link = models.URLField(blank=True)

    def __str__(self):
        return f'{self.name} - Added time: {self.created_at}'

class Platform(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class ProductPlatform(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    link = models.URLField(blank=True)

    def __str__(self):
        return f'{self.product.name} - {self.platform.name} - Price: {self.price}'
