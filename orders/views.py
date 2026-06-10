from django.shortcuts import render, get_object_or_404, redirect
from products.models import Product
from decimal import Decimal
from datetime import datetime
import razorpay
from django.conf import settings
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')

def payment_page(request):

    amount = Decimal(request.session.get('total', '0'))

    if amount <= 0:
        return redirect('checkout')

    client = razorpay.Client(
        auth=(
            settings.RAZORPAY_KEY_ID,
            settings.RAZORPAY_KEY_SECRET
        )
    )

    payment = client.order.create({
        "amount": int(amount * 100),
        "currency": "INR",
        "payment_capture": "1"
    })

    return render(request, "orders/payment.html", {
        "payment": payment,
        "amount": amount,
        "razorpay_key": settings.RAZORPAY_KEY_ID
    })

@login_required(login_url='login')

def checkout(request):

    cart_items = []
    subtotal = Decimal('0.00')

    buy_now = request.session.get('buy_now')

    if buy_now:
        product = get_object_or_404(Product, id=buy_now['product_id'])

        item_total = product.price
        subtotal = item_total

        cart_items = [{
            'product': product,
            'quantity': 1,
            'size': buy_now.get('size'),
            'subtotal': item_total
        }]

    else:
       
        cart = request.session.get('cart', {})

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

    if request.method == 'POST':
        request.session['customer_name'] = request.POST.get('name')
        request.session['phone'] = request.POST.get('phone')
        request.session['address'] = request.POST.get('address')
        request.session['city'] = request.POST.get('city')
        request.session['pincode'] = request.POST.get('pincode')

        request.session['total'] = str(total)

        return redirect('payment')

    return render(request, 'orders/checkout.html', {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping': shipping,
        'tax': tax,
        'total': total,
    })

@login_required(login_url='login')

def payment(request):

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')

        request.session['payment_method'] = payment_method

        return redirect('order_success')

    return render(request, 'orders/payment.html')

def order_success(request):

    order = {
        'order_number': 'SHOE12345',
        'total_amount': request.session.get('total', '0'),
        'status': 'Confirmed',
        'payment_method': request.session.get('payment_method', 'COD'),
        'created_at': datetime.now(),
        'customer_name': request.session.get('customer_name'),
        'phone': request.session.get('phone'),
        'address': request.session.get('address'),
        'city': request.session.get('city'),
        'pincode': request.session.get('pincode'),
    }

    request.session.pop('buy_now', None)

    return render(request, 'orders/order_success.html', {
        'order': order
    })

def track_order(request):

    order_number = request.GET.get('order_number')

    order = None

    if order_number:
        order = {
            'order_number': order_number,
            'status': 'Shipped',
            'current_location': 'Kochi Hub',
            'estimated_delivery': '2 Days'
        }

    return render(request, 'orders/track_order.html', {
        'order': order
    })

def payment_success(request):
    return render(request, "orders/payment_success.html")