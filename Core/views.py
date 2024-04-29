from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, HttpResponse
from bs4 import BeautifulSoup
import requests
from .models import Product, ProductPlatform

def dashboard(request):
    return render(request, 'dashboard.html')

def homepage(request):
    return render(request, 'homepage.html')

def categories(request):
    return render(request, 'categories.html')

def login(request):
    return render(request, 'login.html')

def login1(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['password']
        user = auth.authenticate(username=username, password=pass1)
        if user is not None:
            auth.login(request, user)
            return render(request, 'dashboard.html')
        else:
            messages.info(request, 'Invalid credentials')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

def register1(request):
    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['password']
        pass2 = request.POST['password1']
        if pass1 == pass2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'OOPS! Username already taken')
                return render(request, 'register.html')
            else:
                user = User.objects.create_user(username=username, password=pass1)
                user.save()
                messages.info(request, 'Account created successfully!!')
                return render(request, 'login.html')
        else:
            messages.info(request, 'Passwords do not match')
            return render(request, 'register.html')

@login_required
def logout(request):
    auth.logout(request)
    messages.info(request, 'You have been successfully logged out.')
    return render(request, 'homepage.html')

def products(request):
    all_products = Product.objects.all()
    paginator = Paginator(all_products, 9)  # 9 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'products.html', {'page_obj': page_obj})
def scrape_and_update_price(product):
    platforms = ProductPlatform.objects.filter(product=product)
    for platform in platforms:
        response = requests.get(platform.link)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            price_element = soup.find('span', class_='price')
            if price_element:
                price = price_element.text.strip()
                platform.price = price
                platform.save()

def update_price(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    scrape_and_update_price(product)
    return HttpResponse("Prices updated successfully!")

from django.shortcuts import render, get_object_or_404
from .models import Product

def product_description(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    formatted_description = product.description.replace("->", "<br>")

    # Track last viewed products in session
    last_product_viewed = request.session.get('last_product_viewed', [])
    if not isinstance(last_product_viewed, list):
        last_product_viewed = [last_product_viewed]
    if product_id not in last_product_viewed:
        last_product_viewed.append(product_id)
    last_product_viewed = last_product_viewed[-4:]
    request.session['last_product_viewed'] = last_product_viewed

    # Retrieve last viewed products (excluding current product)
    last_viewed_products = Product.objects.filter(pk__in=last_product_viewed).exclude(pk=product_id)

    context = {
        'product': product,
        'last_viewed_products': last_viewed_products,
        'formatted_description': formatted_description,
    }
    return render(request, 'product_description.html', context)
