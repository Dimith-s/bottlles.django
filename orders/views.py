from django.shortcuts import render,redirect
from django.http import HttpResponse
from carts.models import cartitem,cart
from .forms import OrderForm
import datetime
from .models import Order,OrderProduct,Payment
from accounts.models import Address
from store.models import product
import razorpay
from django.conf import settings
from .models import Order
from store.models import coupon
from django.contrib import messages
from .models import Wallet
from decimal import Decimal
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
    print('reqst:',request.POST)
    discount = request.POST.get('discount_price')
    print(discount)
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
                total += (cart_item.product.original_price() * cart_item.quantity)
                quantity += cart_item.quantity
            try:
                discount = float(discount)
            except (TypeError, ValueError):
            # Handle the case where discount is not a valid numeric value
                discount = 0.0 
            tax = (2*total)/100
            grand_total = total + tax - discount
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
            data.is_ordered = True
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
            current_user = request.user
            address_id = request.POST['adress_id']
            address = Address.objects.get(id=address_id)
            cart_items = cartitem.objects.filter(user=current_user)

            # Calculate the total amount to be deducted from the wallet
            for cart_item in cart_items:
                total += (cart_item.product.original_price() * cart_item.quantity)
                quantity += cart_item.quantity
            try:
                discount = float(discount)
            except (TypeError, ValueError):
                discount = 0.0

            tax = (2 * total) / 100
            grand_total = total + tax - discount

            # Get or create the user's wallet
            wallet = Wallet.objects.get(user=current_user)
            print('wallet:',wallet.balance)

            # Check if the user has enough balance in their wallet
            if wallet.balance >= grand_total:
                # Deduct the amount from the user's wallet balance
                wallet.balance -= Decimal(str(grand_total))
                wallet.save()
                payment = Payment(
                user = current_user,
                payment_id = 'wallet_10000',
                payment_method = 'wallet',
                amount_paid = grand_total,
                status = 'walletpaid'

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
                data.is_ordered = True
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



               

                # ... Your existing code to complete the order ...

                return render(request, 'orderr/order_complete.html', context)
            else:
                # Handle the case where the wallet balance is insufficient
                return render(request, 'orderr/insufficient_balance.html')
            print("2")
        elif payment_option == 'razorpay':
            discount = request.POST.get('discount_price')
            print('discount : ', discount)
            current_user = request.user
            address_id = request.POST['adress_id']
            print('address id : ', address_id)
            address = Address.objects.get(id=address_id)
            cart_items = cartitem.objects.filter(user=current_user)
            for cart_item in cart_items:
                total += (cart_item.product.original_price() * cart_item.quantity)
                quantity += cart_item.quantity
            try:
                discount = float(discount)
            except (TypeError, ValueError):
            # Handle the case where discount is not a valid numeric value
                discount = 0.0
            
            tax = (2*total)/100
            grand_total = total + tax - discount
            print('dimith:',grand_total)
            grand_total_price = int(grand_total)
            print(grand_total_price)
            client = razorpay.Client(auth=(settings.KEY, settings.SECRET))
            print(client)
            payment = client.order.create({'amount':grand_total_price*100,'currency':'INR','payment_capture':1})
            context = {'payment':payment,
                    'order':cart_items,
                    'address':address,
                    'discount':int(discount),
                      
                      }
            print('hai')
            print('brpp')
            
            
            return render(request,'orderr/razo.html',context)
    return render(request,'home.html')

def razorpay_payment(request,id,discount_amount):
    print('discount_amount : ', discount_amount)
    current_user =request.user
    discount = discount_amount
    address = Address.objects.get(id=id)
    
    cart_items = cartitem.objects.filter(user=current_user)                     
    cart_count = cart_items.count()         
    if cart_count <= 0:  
        return redirect('store')
    grand_total= 0
    tax = 0
    total=0
    quantity=0
    for cart_item in cart_items:
        total += (cart_item.product.original_price() * cart_item.quantity)
        quantity += cart_item.quantity
    try:
        discount = float(discount)
    except (TypeError, ValueError):
    # Handle the case where discount is not a valid numeric value
        discount = 0.0
    

    tax = (2*total)/100
    grand_total = total + tax - discount
    print('pay',grand_total)
         
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
    data.is_ordered = True
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

            
    return render(request,'orderr/order_complete.html',context) 
            

def add_coupon(request):
    total=0
    quantity = 0
    discount_price = False
    try:
        if request.user.is_authenticated:
            cart_items = cartitem.objects.filter(user=request.user,is_active=True)
        else:
            cart_model = cart.objects.get(cart_id = _cart_id(request))
            print(cart_model)
            cart_items = cartitem.objects.filter(cart=cart_model,is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.original_price() * cart_item.quantity)
            quantity += cart_item.quantity
            
    except cart.DoesNotExist:
        pass
    grand_total = 0
    cart_items = cartitem.objects.filter(user=request.user)
    for cart_item in cart_items:
        grand_total += (cart_item.product.original_price() * cart_item.quantity)
    
    if request.method=="POST":
        coupon_code = request.POST.get('Coupon')
        print('coupon:',coupon_code)
        try:
            coupon_obj = coupon.objects.get(coupon_code=coupon_code)
            print('dim:',coupon_obj)
            if not coupon_obj.is_expired:
                if grand_total >= coupon_obj.minimum_amount:
                    # Calculate the discount based on the coupon
                    discount_amount = coupon_obj.discount_price
                    grand_total -= discount_amount
                    print(grand_total)
                    discount_price = discount_amount
                    # Store the applied coupon code in the user's session or database
                    request.session["applied_coupon"] = coupon_code
                    print('session:',request.session["applied_coupon"])
                    print('Session Data in add_coupon view:', request.session)
                    request.session.save()
                    messages.success(request, f"Coupon '{coupon_code}' applied successfully. Discount: {discount_amount}")
                else:
                    messages.error(request, "Coupon minimum amount condition not met.")
                    request.session.pop("applied_coupon", None)
            else:
                messages.error(request, "Coupon is expired.")
                request.session.pop("applied_coupon", None)
            
            request.session.save()
        except coupon.DoesNotExist:
            messages.warning(request, "Invalid coupon code.")
            request.session.pop("applied_coupon", None)
    
    print('last:',request.session)
    context={
        'total': total,
        'quantity': quantity,
        'cart_items':cart_items,
        'discount_price': discount_price,
        'grand_total': grand_total,
    }
    return render(request,'store/cart.html',context)
           
            
            
            
            
            
            
            
   
       
       
            


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
       

    
def order_complete(request,id):
    print('id:',id)
    
    orders = Order.objects.get(user=request.user,id=id)
    orderproducts = OrderProduct.objects.filter(order=orders)
    
    context ={
        'order':orders,
        'ordered_products':orderproducts,
    }
    return render(request,'orderr/order_complete.html',context)

def cancel_order(request, id):
    try:
        order = Order.objects.get(id=id, user=request.user)
        print('id:',id)
        print(order)
        # Assuming you have a "status" field in your Order model, change its value here
        order.status = 'Cancelled'  # You need to update this based on your model structure
        print(order.status)
        order.save()
        return redirect('dashboard')  # Redirect back to the order complete page
    except Order.DoesNotExist:
        # Handle the case where the order doesn't exist or the user is not authorized
        return redirect('some_error_page')



def return_request(request,id):
    if request.method == "POST":
        print(id)
        order = Order.objects.get(pk=id)
        
        order.status = 'Return requested'
        order.save()

    if order.status == 'accepted':
        print('status:',order.status)
        wallet = Wallet.objects.get(user_id=orderproduct.order.user.id)
        wallet.balance += orderproduct.total()
        wallet.save()

    return redirect('dashboard')    

