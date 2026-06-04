from django.urls import path
from .views import (
    checkout,
    payment_page,
    payment,
    order_success,
    track_order,
)

urlpatterns = [
    path('checkout/', checkout, name='checkout'),
 
    path('payment/', payment_page, name='payment'),

    path('payment-method/', payment, name='payment_method'),

    path('order-success/', order_success, name='order_success'),

    path('track/', track_order, name='track_order'),
]