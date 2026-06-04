from django.shortcuts import render, redirect
from products.models import Product


# =========================
# ADD TO WISHLIST
# =========================
def add_to_wishlist(request, product_id):
    wishlist = request.session.get('wishlist', [])

    product_id = int(product_id)

    if product_id not in wishlist:
        wishlist.append(product_id)

    request.session['wishlist'] = wishlist
    request.session.modified = True

    return redirect('wishlist_detail')


# =========================
# WISHLIST DETAIL PAGE
# =========================
def wishlist_detail(request):
    wishlist = request.session.get('wishlist', [])

    # convert safely to int list
    wishlist_ids = [int(i) for i in wishlist]

    products = Product.objects.filter(id__in=wishlist_ids)

    return render(request, 'wishlist/wishlist_detail.html', {
        'products': products
    })


# =========================
# REMOVE FROM WISHLIST
# =========================
def remove_from_wishlist(request, item_id):
    wishlist = request.session.get('wishlist', [])

    item_id = int(item_id)

    if item_id in wishlist:
        wishlist.remove(item_id)

    request.session['wishlist'] = wishlist
    request.session.modified = True

    return redirect('wishlist_detail')