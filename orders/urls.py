from django.urls import path
from . import views

urlpatterns = [
    # path('place_order/',views.place_order,name='place_order'),
    path('order_complete/',views.order_complete,name='order_complete'),
    path('payment_method/',views.payment_method,name='payment_method'),
    path('razorpay_payment /<int:id>/',views.razorpay_payment,name='razorpay_payment'),
    
    
]
