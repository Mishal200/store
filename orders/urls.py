from django.urls import path
from .views import (
    checkout,
    payment,
    order_success,
    track_order
)

urlpatterns = [
    path('checkout/', checkout, name='checkout'),
    path('payment/', payment, name='payment'),
    path('success/', order_success, name='order_success'),
    path('track/', track_order, name='track_order'),
]