from django.shortcuts import render,redirect
from store.models import product
from .models import cart,cartitem
from django.http import HttpResponse 
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.models import Address
from django.http import HttpResponse

# Create your views here.
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request,product_id):
    prod = product.objects.get(id=product_id)#get the product
    print('product : ',prod)
    try:
        cart_model = cart.objects.get(cart_id=_cart_id(request))# get the cart using the cart_id preent in session
    except cart.DoesNotExist:
        cart_model = cart.objects.create(
            cart_id = _cart_id(request)
        )
        cart_model.save()

    try:
        cart_item = cartitem.objects.get(product=prod,cart=cart_model)
        cart_item.quantity +=1 #cart_item.quantity = cart_item.quantity + 1
        cart_item.save()
    except cartitem.DoesNotExist:
        cart_item = cartitem.objects.create(
            product = prod,
            quantity = 1,
            cart = cart_model,
        )
        cart_item.save()
    
    return redirect('cart_page')

def remove_cart(request,product_id):
    cart_model = cart.objects.get(cart_id=_cart_id(request))
    Product = get_object_or_404(product,id=product_id)
    cart_item = cartitem.objects.get(product=Product,cart=cart_model)

    if cart_item.quantity > 1:
        cart_item.quantity -=1
        cart_item.save()

    else:
        cart_item.delete()
    return redirect('cart_page')

def remove_cart_item(request,product_id):
    cart_model = cart.objects.get(cart_id=_cart_id(request))
    Product = get_object_or_404(product,id = product_id)
    cart_item = cartitem.objects.get(product = Product,cart = cart_model)
    cart_item.delete()
    return redirect('cart_page')

    

def cart_page(request,total=0,quantity=0,cart_items=None):
    try:
        
        cart_model = cart.objects.get(cart_id = _cart_id(request))
        cart_items = cartitem.objects.filter(cart=cart_model,is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.prize * cart_item.quantity)
            quantity += cart_item.quantity
    except cart.DoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items':cart_items
    }
    return render(request,'store/cart.html',context)



@login_required(login_url='login')
def checkout(request,total=0,quantity=0,cart_items=None):
    try:
        cart_model = cart.objects.get(cart_id = _cart_id(request))
        cart_items = cartitem.objects.filter(cart=cart_model,is_active=True)
        user = request.user
        address = Address.objects.filter(user=user)
        print(address)
        for cart_item in cart_items:
            total += (cart_item.product.prize * cart_item.quantity)
            quantity += cart_item.quantity
    except cart.DoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items':cart_items,
        'address' : address,
    }
    return render(request,'store/checkout.html',context)










def order_success(request):
    return HttpResponse("ordersuccess")