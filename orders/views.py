from django.shortcuts import render,redirect
from django.http import HttpResponse
from carts.models import cartitem

import datetime
from .models import Order

# Create your views here.
# def place_order(request,total=0,quantity=0):
#     current_user = request.user
#     print(current_user)

#     #if the cart count is less than or equal to zero, then redirect to the shop
#     cart_items = cartitem.objects.filter(user=current_user)
    
#     cart_count = cart_items.count()
#     print(cart_count)

#     if cart_count <= 0:
#         return redirect('store')
    
#     grand_total= 0
#     tax = 0
#     for cart_item in cart_items:
#         total += (cart_item.product.prize * cart_item.quantity)
#         quantity += cart_item.quantity
#     tax = (2*total)/100
#     grand_total = total + tax
    
    

#     if request.method=='POST':
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             #store all the billing information inside order table
#             data = Order()
#             data.user = current_user
#             data.first_name = form.cleaned_data['first_name']
#             print('1')
#             data.last_name = form.cleaned_data['last_name']
#             data.phone = form.cleaned_data['phone']
#             data.email = form.cleaned_data['email']
#             data.address_line_1 = form.cleaned_data['address_line_1']
#             data.address_line_2 = form.cleaned_data['address_line_2']
#             data.country = form.cleaned_data['country']
#             data.state = form.cleaned_data['state']
#             data.city = form.cleaned_data['city']
#             data.order_note = form.cleaned_data['order_note']
#             data.order_total = grand_total
#             data.tax = tax
#             data.ip = request.META.get('REMOTE_ADDR')
#             data.save()

#             #generate the order number
#             yr = int(datetime.date.today().strftime('%Y'))
#             dt = int(datetime.date.today().strftime('%d'))
#             mt = int(datetime.date.today().strftime('%m'))

#             d = datetime.date(yr,mt,dt)
#             current_date = d.strftime("%Y%m%d")
#             order_number = current_date + str(data.id)
#             data.order_number = order_number
#             data.save()
#             return redirect('checkout')
#         else:
#             return redirect('home')
    