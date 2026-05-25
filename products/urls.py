from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='home'),  
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('wishlist/', views.wishlist, name='wishlist'),
]