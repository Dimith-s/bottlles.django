from django.urls import path
from . import views

urlpatterns = [
    # path('place_order/',views.place_order,name='place_order'),
    path('order_complete/<int:id>/',views.order_complete,name='order_complete'),
    path('payment_method/',views.payment_method,name='payment_method'),
    # path('razorpay_payment /<int:id>/',views.razorpay_payment,name='razorpay_payment'),
    path('razorpay_payment /<int:id>/<int:discount_amount>/',views.razorpay_payment,name='razorpay_payment'),
    path('add_coupon/', views.add_coupon, name='add_coupon'),
    path('cancel_order/<int:id>/', views.cancel_order, name='cancel_order'),
    path('return_request/<int:id>/', views.return_request, name='return_request'),  
    
    
]
