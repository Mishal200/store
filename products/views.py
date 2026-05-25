from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Product


def product_list(request):
    products = Product.objects.filter(available=True)

    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(brand__icontains=query)
        )

    return render(request, 'products/product_list.html', {
        'products': products
    })


def product_detail(request, id):
    product = get_object_or_404(Product, id=id, available=True)
    return render(request, 'products/product_detail.html', {
        'product': product
    })


def wishlist(request):
    return render(request, 'wishlist/wishlist_detail.html')