from django.shortcuts import render,redirect
from django.http import HttpResponse
from carts.models import cartitem
from .forms import OrderForm
import datetime
from .models import Order,OrderProduct,Payment
from accounts.models import Address
from store.models import product
import razorpay
from django.conf import settings

#Create your views here.
# def place_order(request,total=0,quantity=0):

#     current_user = request.user
#     print(current_user)

#     #if the cart count is less than or equal to zero, then redirect to the shop
#     cart_items = cartitem.objects.filter(user=current_user)
#     print(cart_items.query)
    
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


# def place_order(request,total=0,quantity=0):
#     print('POST : ', request.POST)
#     address_id = request.POST['adress_id']
#     print('address id : ', address_id)
#     address = Address.objects.get(id=address_id)
#     print('address : ', address)
#     current_user = request.user

#     #if the cart count is less than or equal to zero, then redirect to the shop
#     cart_items = cartitem.objects.filter(user=current_user)
    
    
#     cart_count = cart_items.count()
    

#     if cart_count <= 0:
#         return redirect('store')
    
#     grand_total= 0
#     tax = 0
#     for cart_item in cart_items:
#         total += (cart_item.product.prize * cart_item.quantity)
#         quantity += cart_item.quantity
#     tax = (2*total)/100
#     grand_total = total + tax
#     payment = Payment(
#         user = current_user,
#         payment_id = 'Cod_10000',
#         payment_method = 'COD',
#         amount_paid = grand_total,
#         status = 'Pending'
#     )
#     payment.save()
#     data = Order()
#     data.payment = payment
#     data.user = current_user
#     data.first_name = address.name
#     data.last_name = address.last_name
#     data.phone = address.phone
#     data.email = request.user.email
#     data.address_line_1= address.address
#     data.city = address.city
#     data.state = address.state
#     data.country = 'India'
#     data.order_total = grand_total
#     data.tax = tax
#     data.ip = request.META.get('REMOTE_ADDR')
#     data.save()

#     yr = int(datetime.date.today().strftime('%Y'))
#     dt = int(datetime.date.today().strftime('%d'))
#     mt = int(datetime.date.today().strftime('%m'))

#     d = datetime.date(yr,mt,dt)
#     current_date = d.strftime("%Y%m%d")
#     order_number = current_date + str(data.id)
#     data.order_number = order_number
#     data.save()
    
#     for item in cart_items:
#         orderproduct =OrderProduct()
#         orderproduct.order = data
#         orderproduct.Product = item.product
#         orderproduct.quantity =item.quantity
#         orderproduct.product_price = item.sub_total()
#         orderproduct.ordered = True
#         orderproduct.save()

#         prod = product.objects.get(id = item.product.id)
#         prod.stock -= item.quantity
#         prod.save()

#     cart_items.delete()
#     orderproducts = OrderProduct.objects.filter(order=data)
    

#     context = {
#         'order':data,
#         'payment':payment,
#         'ordered_products':orderproducts,
#         'subtotal':total,
#     }

    
#     return render(request,'orderr/order_complete.html', context)

def payment_method(request,total=0, quantity=0):
    if request.method == 'POST':
        payment_option = request.POST.get('payment_option')
        
        if payment_option == 'cod':
            address_id = request.POST['adress_id']
            print('address id : ', address_id)
            address = Address.objects.get(id=address_id)
            print('address : ', address)
            current_user = request.user

            #if the cart count is less than or equal to zero, then redirect to the shop
            cart_items = cartitem.objects.filter(user=current_user)
            
            
            cart_count = cart_items.count()
            

            if cart_count <= 0:
                return redirect('store')
            
            grand_total= 0
            tax = 0
            for cart_item in cart_items:
                total += (cart_item.product.prize * cart_item.quantity)
                quantity += cart_item.quantity
            tax = (2*total)/100
            grand_total = total + tax
            payment = Payment(
                user = current_user,
                payment_id = 'Cod_10000',
                payment_method = 'COD',
                amount_paid = grand_total,
                status = 'Pending'
            )
            payment.save()
            data = Order()
            data.payment = payment
            data.user = current_user
            data.first_name = address.name
            data.last_name = address.last_name
            data.phone = address.phone
            data.email = request.user.email
            data.address_line_1= address.address
            data.city = address.city
            data.state = address.state
            data.country = 'India'
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))

            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()
            
            for item in cart_items:
                orderproduct =OrderProduct()
                orderproduct.order = data
                orderproduct.Product = item.product
                orderproduct.quantity =item.quantity
                orderproduct.product_price = item.sub_total()
                orderproduct.ordered = True
                orderproduct.save()

                prod = product.objects.get(id = item.product.id)
                prod.stock -= item.quantity
                prod.save()

            cart_items.delete()
            orderproducts = OrderProduct.objects.filter(order=data)
            
            

            context = {
                'order':data,
                'payment':payment,
                'ordered_products':orderproducts,
                'subtotal':total,
                
            }

            
            return render(request,'orderr/order_complete.html', context)

            
        elif payment_option == 'wallet':
            print("2")
        elif payment_option == 'razorpay':
            current_user = request.user
            address_id = request.POST['adress_id']
            print('address id : ', address_id)
            address = Address.objects.get(id=address_id)
            cart_items = cartitem.objects.filter(user=current_user)
            for cart_item in cart_items:
                total += (cart_item.product.prize * cart_item.quantity)
                quantity += cart_item.quantity
            tax = (2*total)/100
            grand_total = total + tax
            print('dimith:',grand_total)
            grand_total_price = int(grand_total)
            print(grand_total_price)
            client = razorpay.Client(auth=(settings.KEY, settings.SECRET))
            print(client)
            payment = client.order.create({'amount':grand_total_price*100,'currency':'INR','payment_capture':1})
            context = {'payment':payment,
                    'order':cart_items,
                    'address':address,
                      
                      }
            print('hai')
            print('brpp')
            return render(request,'orderr/razo.html',context)
    return render(request,'home.html')

def razorpay_payment(request,id):
    address = Address.objects.get(id=id)
    current_user =request.user
    cart_items = cartitem.objects.filter(user=current_user)                     
    cart_count = cart_items.count()         
    if cart_count <= 0:  
        return redirect('store')
    grand_total= 0
    tax = 0
    total=0
    quantity=0
    for cart_item in cart_items:
        total += (cart_item.product.prize * cart_item.quantity)
        quantity += cart_item.quantity

    tax = (2*total)/100
    grand_total = total + tax      
    payment = Payment(
                    user = current_user,
                    payment_id = 'Razor_10000',
                    payment_method = 'Razorpay',
                    amount_paid = grand_total,
                    status = 'Success'
                )   
    payment.save()   

    data = Order()
    data.payment = payment
    data.user = current_user
    data.first_name = address.name
    data.last_name = address.last_name
    data.phone = address.phone
    data.email = request.user.email
    data.address_line_1= address.address
    data.city = address.city
    data.state = address.state
    data.country = 'India'
    data.order_total = grand_total
    data.tax = tax
    data.ip = request.META.get('REMOTE_ADDR')
    data.save()

    yr = int(datetime.date.today().strftime('%Y'))
    dt = int(datetime.date.today().strftime('%d'))
    mt = int(datetime.date.today().strftime('%m'))

    d = datetime.date(yr,mt,dt)
    current_date = d.strftime("%Y%m%d")
    order_number = current_date + str(data.id)
    data.order_number = order_number
    data.save()
    for item in cart_items:
        orderproduct =OrderProduct()
        orderproduct.order = data
        orderproduct.Product = item.product
        orderproduct.quantity =item.quantity
        orderproduct.product_price = item.sub_total()
        orderproduct.ordered = True
        orderproduct.save()

        prod = product.objects.get(id = item.product.id)
        prod.stock -= item.quantity
        prod.save()

    cart_items.delete()
    orderproducts = OrderProduct.objects.filter(order=data)
    print("ordercompleted")
    context = {
                'order':data,
                'payment':payment,
                'ordered_products':orderproducts,
                'subtotal':total,
                
            }

            
    return render(request,'orderr/order_complete.html', context) 
            
            
            
            
            
            
            
            
            
            
   
       
       
            


#     if request.method == 'POST':
#         current_user = request.user
#         cart_items = cartitem.objects.filter(user=current_user)
#         total = 0
#         quantity = 0
#         for cart_item in cart_items:
            
#             total += (cart_item.product.prize * cart_item.quantity)
#             quantity += cart_item.quantity
#         tax = (2 * total) / 100
#         grand_total = total + tax
#         grand_total_price = int(grand_total)
        
#         client = razorpay.Client(auth=(settings.KEY,settings.SECRET))
#         payment = client.order.create({
#             'amount': grand_total_price*100,
#             'currency': 'INR',
#             'payment_capture': 1
#         })

#         print('razoo:',payment)
#         context = {'payment':payment}
#         print('hai')
#         return render(request,'store/store.html',context)
#     return render(request,'home.html')
    




# def place_order(request, total=0, quantity=0):
#     print('POST : ', request.POST)
#     address_id = request.POST['adress_id']
#     print('address id : ', address_id)
#     address = Address.objects.get(id=address_id)
#     print('address : ', address)
#     current_user = request.user

#     #if the cart count is less than or equal to zero, then redirect to the shop
#     cart_items = cartitem.objects.filter(user=current_user)
    
    
#     cart_count = cart_items.count()
    

#     if cart_count <= 0:
#         return redirect('store')
    
#     grand_total= 0
#     tax = 0
#     for cart_item in cart_items:
#         total += (cart_item.product.prize * cart_item.quantity)
#         quantity += cart_item.quantity
#     tax = (2*total)/100
#     grand_total = total + tax
#     payment = Payment(
#         user = current_user,
#         payment_id = 'Cod_10000',
#         payment_method = 'COD',
#         amount_paid = grand_total,
#         status = 'Pending'
#     )
#     payment.save()
#     data = Order()
#     data.payment = payment
#     data.user = current_user
#     data.first_name = address.name
#     data.last_name = address.last_name
#     data.phone = address.phone
#     data.email = request.user.email
#     data.address_line_1= address.address
#     data.city = address.city
#     data.state = address.state
#     data.country = 'India'
#     data.order_total = grand_total
#     data.tax = tax
#     data.ip = request.META.get('REMOTE_ADDR')
#     data.save()

#     yr = int(datetime.date.today().strftime('%Y'))
#     dt = int(datetime.date.today().strftime('%d'))
#     mt = int(datetime.date.today().strftime('%m'))

#     d = datetime.date(yr,mt,dt)
#     current_date = d.strftime("%Y%m%d")
#     order_number = current_date + str(data.id)
#     data.order_number = order_number
#     data.save()
    
#     for item in cart_items:
#         orderproduct =OrderProduct()
#         orderproduct.order = data
#         orderproduct.Product = item.product
#         orderproduct.quantity =item.quantity
#         orderproduct.product_price = item.sub_total()
#         orderproduct.ordered = True
#         orderproduct.save()

#         prod = product.objects.get(id = item.product.id)
#         prod.stock -= item.quantity
#         prod.save()

#     cart_items.delete()
#     orderproducts = OrderProduct.objects.filter(order=data)
    
    

#     context = {
#         'order':data,
#         'payment':payment,
#         'ordered_products':orderproducts,
#         'subtotal':total,
        
#     }

    
#     return render(request,'orderr/order_complete.html', context)
       

    
def order_complete(request):
    return render(request,'orderr/order_complete.html')

