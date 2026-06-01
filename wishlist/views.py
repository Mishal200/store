from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product

def add_to_wishlist(request, product_id):
    product_id = str(product_id)

    wishlist = request.session.get('wishlist', [])

    if product_id not in wishlist:
        wishlist.append(product_id)

    request.session['wishlist'] = wishlist

    return redirect('wishlist_detail')

def wishlist_detail(request):
    wishlist = request.session.get('wishlist', [])

    products = Product.objects.filter(id__in=wishlist)

    return render(request, 'wishlist/wishlist_detail.html', {
        'products': products
    })

def remove_from_wishlist(request, product_id):
    wishlist = request.session.get('wishlist', [])

    product_id = str(product_id)

    if product_id in wishlist:
        wishlist.remove(product_id)

    request.session['wishlist'] = wishlist

    return redirect('wishlist_detail')