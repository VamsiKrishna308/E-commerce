from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from Core.models import Product

def search_products(request):
    search_term = request.GET.get('searchTerm')
    if search_term:
        search_term = search_term.lower()
        # Find the product with the exact name matching the search term
        try:
            product = Product.objects.get(name__iexact=search_term)
            product_id = product.id
            return redirect(reverse('product_description', args=[product_id]))
        except Product.DoesNotExist:
            return redirect('products')
    else:
        return render(request, 'search_form.html')

def product_description(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    formatted_description = product.description.replace("->", "<br> <br> <br>")
    last_product_viewed = request.session.get('last_product_viewed', [])

    # Ensure last_product_viewed is always a list
    if not isinstance(last_product_viewed, list):
        last_product_viewed = [last_product_viewed]

    # Append the current product ID to the list of last viewed products
    if product_id not in last_product_viewed:
        last_product_viewed.append(product_id)

    # Limit the list to the last 4 viewed products
    last_product_viewed = last_product_viewed[-4:]

    # Update the session variable
    request.session['last_product_viewed'] = last_product_viewed

    # Retrieve the product objects for the last viewed products
    last_viewed_products = Product.objects.filter(pk__in=last_product_viewed)

    # Ensure the current product is not included in the last viewed products
    last_viewed_products = last_viewed_products.exclude(pk=product_id)

    return render(request, 'product_description.html', {'product': product, 'last_viewed_products': last_viewed_products,'formatted_description': formatted_description})



def price_comparison(request):
    if request.method == 'POST':
        # Handle form submission for selected products
        num_products_to_compare = int(request.POST.get('num_products', 2))  # Default to 2
        num_products_to_compare = min(max(num_products_to_compare, 2), 4)  # Clamp between 2 and 4

        selected_products = [request.POST.get(f'selected_products_{i}') for i in range(1, num_products_to_compare + 1)]

        # Implement price comparison logic for the selected products
        product_prices = {}
        for product_name in selected_products:
            try:
                product = Product.objects.get(name=product_name)
                formatted_features = "<br><br>".join(product.features.split("~"))
                product_prices[product_name] = {'price': product.price, 'features': formatted_features}
                # Replace with your logic to fetch additional product features if needed
            except Product.DoesNotExist:
                pass  # Handle the case where the product doesn't exist

        return render(request, 'price_comparison_results.html', {'product_prices': product_prices})

    # Initial rendering of price comparison page
    num_products_to_compare = int(request.POST.get('num_products', 2))  # Default to 2
    num_products_to_compare = min(max(num_products_to_compare, 2), 4)  # Clamp between 2 and 4

    # Fetch all product names for the dropdown menu
    product_names = [product.name for product in Product.objects.all()]

    # Create a range of numbers based on num_products_to_compare
    num_products_to_range = range(1, num_products_to_compare + 1)

    return render(request, 'price_comparison.html', {'product_names': product_names,
                                                     'num_products_to_range': num_products_to_range,
                                                     'num_products_to_compare': num_products_to_compare})