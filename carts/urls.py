from django.urls import path
from .import views

urlpatterns = [
    path('', views.cart_page,name='cart_page'),
    path('add_cart/<int:product_id>/',views.add_cart,name = 'add_cart'),
    path('remove_cart/<int:product_id>/',views.remove_cart,name = 'remove_cart'),
    path('remove_cart_item/<int:product_id>/',views.remove_cart_item,name='remove_cart_item'),
    path('checkout',views.checkout,name='checkout'),
    path('order_success',views.order_success,name='order_success'),
    
    
]