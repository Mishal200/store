from django.shortcuts import render, get_object_or_404
from products.models import Product
from decimal import Decimal

def checkout(request):
    cart = request.session.get('cart', {})

    cart_items = []
    subtotal = Decimal('0.00')

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=int(product_id))

        item_total = product.price * quantity
        subtotal += item_total

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': item_total
        })

    shipping = Decimal('50.00') if cart_items else Decimal('0.00')
    tax = subtotal * Decimal('0.10')
    total = subtotal + shipping + tax

    return render(request, 'cart/checkout.html', {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping': shipping,
        'tax': tax,
        'total': total,
    })

def track_order(request):
    order = None
    order_number = request.GET.get('order_number')

    if order_number:
        try:
            order = Order.objects.get(order_number=order_number)
        except Order.DoesNotExist:
            order = None

    return render(request, 'orders/track_order.html', {
        'order': order,
        'order_number': order_number,
    })