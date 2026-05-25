from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from products.models import Product


# -------------------------
# ADD TO CART (NO LOGIN)
# -------------------------
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1

    request.session['cart'] = cart

    return redirect('cart')


# -------------------------
# CART VIEW (NO LOGIN)
# -------------------------
def cart_view(request):
    cart = request.session.get('cart', {})

    cart_items = []
    total = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)

        subtotal = product.price * quantity

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })

        total += subtotal

    return render(request, 'cart/cart.html', {
        'cart_items': cart_items,
        'total': total
    })


# -------------------------
# REMOVE FROM CART (NO LOGIN)
# -------------------------
def remove_from_cart(request, item_id):
    cart = request.session.get('cart', {})

    item_id = str(item_id)

    if item_id in cart:
        del cart[item_id]
        request.session['cart'] = cart

    return redirect('cart')


# -------------------------
# CHECKOUT (LOGIN REQUIRED)
# -------------------------
def checkout(request):
    cart = request.session.get('cart', {})

    cart_items = []
    total = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)

        subtotal = product.price * quantity

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })

        total += subtotal

    return render(request, 'cart/checkout.html', {
        'cart_items': cart_items,
        'total': total
    })