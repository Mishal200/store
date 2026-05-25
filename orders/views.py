# from django.shortcuts import render, redirect,get_object_or_404
# from products.models import Product
# from django.contrib.auth.decorators import login_required
# from cart.models import CartItem
# from .models import Order, OrderItem

from django.shortcuts import render, get_object_or_404
from products.models import Product
from decimal import Decimal

# def checkout(request):
    
#     cart_items = CartItem.objects.all()

   
#     if not cart_items.exists():
#         return redirect('cart')

   
#     total = sum(item.subtotal() for item in cart_items)

   
#     order = Order.objects.create(
#         user=request.user,
#         total_amount=total,
#         status='Pending'
        
#     )

    
#     for item in cart_items:
#         OrderItem.objects.create(
#             order=order,
#             product=item.product,
#             quantity=item.quantity,
#             price=item.product.price
#         )

        
#         item.product.stock -= item.quantity
#         item.product.save()

    
#     cart_items.delete()

   
#     return render(request, 'orders/order_success.html', {
#         'order': order
#     })

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