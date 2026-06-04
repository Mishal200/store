from django.urls import path , include
from . import views

urlpatterns = [
    path('', views.product_list, name='home'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
 
    path('add-review/<int:product_id>/', views.add_review, name='add_review'),
]