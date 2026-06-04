from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Product, Review
from django.contrib.auth.decorators import login_required


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

    sizes = product.size.split(',')

    reviews = Review.objects.filter(product=product).order_by('-id')

    return render(request, 'products/product_detail.html', {
        'product': product,
        'sizes': sizes,
        'reviews': reviews
    })

@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        Review.objects.create(
            product=product,
            user=request.user,
            rating=request.POST.get('rating'),
            comment=request.POST.get('comment')
        )

    return redirect('product_detail', id=product_id)