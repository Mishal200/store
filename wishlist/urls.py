from django.urls import path
from . import views

urlpatterns = [
    path('', views.wishlist_detail, name='wishlist_detail'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/', views.wishlist_detail, name='wishlist_detail'),
    path('wishlist/remove/<int:item_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),



]