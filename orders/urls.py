from django.urls import path
from .views import checkout, track_order

urlpatterns = [
    path('checkout/', checkout, name='checkout'),
    path('track/', track_order, name='track_order'),
]