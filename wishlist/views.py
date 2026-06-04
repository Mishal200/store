from django.shortcuts import render, redirect
from products.models import Product


def add_to_wishlist(request, product_id):
    wishlist = request.session.get('wishlist', [])

    product_id = int(product_id)

    if product_id not in wishlist:
        wishlist.append(product_id)

    request.session['wishlist'] = wishlist
    request.session.modified = True

    return redirect('wishlist')   # ✅ FIXED

def wishlist_detail(request):
    wishlist = request.session.get('wishlist', [])

    products = Product.objects.filter(id__in=wishlist)

    return render(request, 'wishlist/wishlist_detail.html', {
        'products': products
    })

def remove_from_wishlist(request, item_id):
    wishlist = request.session.get('wishlist', [])

    item_id = int(item_id)

    if item_id in wishlist:
        wishlist.remove(item_id)

    request.session['wishlist'] = wishlist
    request.session.modified = True

    return redirect('wishlist')   # ✅ FIXED