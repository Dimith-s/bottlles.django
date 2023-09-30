from django.shortcuts import render,redirect
from accounts.models import Accounts
from store.models import product,ProductImage,Size,coupon
from category.models import category
from django.http import JsonResponse
from store.forms import Productform,SizeForm,CouponForm
from category.forms import Categoryform
from orders.models import *
from django.db.models import Count,Sum,Q
from django.utils import timezone
from datetime import datetime,timedelta,date
import datetime
from decimal import Decimal

# Create your views here.
def home(request):

    if request.user.is_superadmin:
        user_count = Accounts.objects.filter(is_superadmin=False).count()
        delivered_products = Order.objects.all().filter(status='Delivered')
        print("delivered_products :",delivered_products)
        revenue = delivered_products.aggregate(Sum('order_total'))['order_total__sum'] or 0
        total_orders = OrderProduct.objects.all().count()
        status_counts = OrderProduct.objects.values('status').annotate(count=Count('status'))
        product_count = product.objects.all().count()
        category_count = category.objects.all().count()
        current_year = timezone.now().year
        order_detail = Order.objects
        monthly_order_count = []
        month = timezone.now().month
        order_detail = Order.objects.filter(
            created_at__lt=date(current_year, 12, 31),
            status='Delivered',
        )

        for i in range(1, month + 1):
            monthly_order = order_detail.filter(created_at__month=i).count()
            monthly_order_count.append(monthly_order)


        today = datetime.datetime.now()
        neworders = Order.objects.filter(created_at__month=today.month).values('created_at__date').annotate(orderitemscount=Count('id', filter=Q(status='Order Placed')))
        cancelledorders = Order.objects.filter(created_at__month=today.month).values('created_at__date').annotate(cancelleditemscount=Count('id',filter=Q(status='Cancelled')))
        returnorders = Order.objects.filter(created_at__month=today.month).values('created_at__date').annotate(returnedorderscount=Count('id', filter=Q(status='accepted')))
        deliveredorders = Order.objects.filter(created_at__month=today.month).values('created_at__date').annotate(delivereditemscount=Count('id', filter=Q(status='Delivered')))

        orderitems = Order.objects.filter(status='Delivered')
        print("orderitems:",orderitems)
        last_date = datetime.datetime.now().date()
        first_date = last_date - timedelta(days=6)
        amount_per_day = []
        date_list = []
        for i in range(1,8):
            total_amount_per_day = 0
            for order in orderitems:
                if order.created_at.date() == first_date:
                    total_amount_per_day += order.order_total
            amount_per_day.append(total_amount_per_day)
            date_list.append(first_date)
            first_date = first_date + timedelta(days=1)
    
  
        context = {
            'revenue':revenue,
            'total_orders':total_orders,
            'status_counts':status_counts,
            'product_count':product_count,
            'category_count':category_count,
            'user_count':user_count,
            'amount_per_day':amount_per_day,
            'date_list':date_list,
            'neworders':neworders,
            'cancelledorders':cancelledorders,
            'returnorders':returnorders,
            'deliveredorders':deliveredorders,
            'monthly_order_count':monthly_order_count,

        }
        return render(request,'admin_temp/adminhome.html', context)
    return redirect('ahome')


def admin_logout(request):
    return redirect('login')

def userlist(request):
    user_list = Accounts.objects.all().order_by('id')
    print(user_list)
    context = {
        'user_list' : user_list
    }
    return render(request,'admin_temp/userlist.html',context)

def productlist(request):
    product_list = product.objects.all().order_by('-id')
    print(product_list)
    context = {
        'product_list' : product_list
    }
    return render(request,'admin_temp/product.html',context)

def sizelist(request):
    size_list = Size.objects.all()
    print('sizelist : ', size_list)
    context = {
        'size_list':size_list,
    }
    return render(request,'admin_temp/size.html',context)

def addsize(request):
    form = SizeForm
    if request.method == 'POST':
        form = SizeForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('sizelist')
    context = {
        'form':form,
    }
    return render(request,'admin_temp/addsize.html',context)


def categorylist(request):
    category_list = category.objects.all().order_by('-id')
    context = {
        'category_list' : category_list
    }
    return render(request,'admin_temp/category.html',context)

def addproduct(request,product_id=0):
    if product_id == 0:
        if request.method=='POST':
            form = Productform(request.POST,request.FILES)
            if form.is_valid():
                productt = form.save()
                if request.FILES.get('pr_images') != 0:
                    images = request.FILES.getlist('pr_images')
                    for img in images:
                        image = ProductImage.objects.create(product=productt, image=img)
                        image.save()
                form.save()
                return redirect('productlist')
            else:
                print('form not valid')
                print(form.errors)
        form = Productform()
    else:
        print('product id : ',product_id)
        prod = product.objects.get(id=product_id)
        form = Productform(instance=prod)
        if request.method == 'POST':
            form = Productform(request.POST, request.FILES,instance=prod)
            if form.is_valid():
                form.save()
                return redirect('productlist')

    context = {
        'form' : form
    }
    return render(request,'admin_temp/addproduct.html',context)

def addcategory(request,category_id=0):
    if category_id==0:
        if request.method=='POST':
            form = Categoryform(request.POST,request.FILES)
            if form.is_valid():
                Category = form.save()
                form.save()
                return redirect('categorylist')
            else:
                print('form is not valid')
                print(form.errors)
        form = Categoryform()
    else:
        cate = category.objects.get(id=category_id)
        form = Categoryform(instance=cate)
        if request.method =='POST':
            form = Categoryform(request.POST,request.FILES,instance=cate)
            if form.is_valid:
                form.save()
                return redirect('categorylist')
    

    context ={
        'form': form
    }
    
    return render(request,'admin_temp/addcategory.html',context)

# user block

def user_block(request, user_id):
    user = Accounts.objects.get(id=user_id)
    if user.is_blocked:
        user.is_blocked = False
        
    else:
        user.is_blocked = True
    user.save()
    return JsonResponse({'msg':'success'})

def category_block(request,category_id):
    user = category.objects.get(id = category_id)
    if user.is_available:
        user.is_available = False
        
    else:
        user.is_available = True
    user.save()
    return JsonResponse({'msg':'success'})

def product_block(request,product_id):
    prod = product.objects.get(id = product_id)
    if prod.is_available:
        prod.is_available = False
    else:
        prod.is_available = True

    prod.save()
    return JsonResponse({'msg':'success'})


# for delete product

def deleteproduct(request,product_id):
    prod = product.objects.get(id=product_id)
    prod.delete()
    return redirect('productlist')

def deletecategory(request,category_id):
    cate = category.objects.get(id=category_id)
    cate.delete()
    return redirect('categorylist')

def orderlist(request):
    order_list = Order.objects.all().order_by('-id')
    context = {
        'order_list' : order_list
    }
    return render(request,'admin_temp/order.html',context)

def order_details(request,id):
   
    main_order = Order.objects.get(pk=id)
    print('honey',main_order)
    orders = OrderProduct.objects.filter(order = main_order).order_by('-id')
    for order in orders:
        print(order.id)

    return render(request,'admin_temp/order_detail.html',{"orders": orders,"id":id,"main_order":main_order})



def edit_order(request, id):
    if request.method == "POST":
        status = request.POST.get("status")
        try:
        
            order = Order.objects.get(pk=id)
            order.status = status
            order.save()
            if status == 'Delivered':
                pyment=order.payment
                pyment.status='Success'
                pyment.save()
            if status == 'accepted':
                user=order.user
                print(user)
                wallet, _ =Wallet.objects.get_or_create(user=user)
                refund_amount= Decimal(str(order.order_total))
                print(refund_amount)
                wallet.balance += refund_amount
                wallet.save()


        except Order.DoesNotExist:
            pass
    return redirect("orderlist")

def coupon_management(request):
    coup = coupon.objects.all()
    context={
        'coup': coup
    } 
    return render(request,'admin_temp/coupon.html',context)

def addcoupon(request):
    form = CouponForm
    if request.method == 'POST':
        form = CouponForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('coupon_management')
    context = {
        'form':form,
    }
    return render(request,'admin_temp/addcoupon.html',context)

    
def sales_report(request):
    orders = OrderProduct.objects.all()
    print("orders :",orders)
    msg = 'nothing'
    if request.method == 'POST':
        start_date = request.POST.get('startDate')
        end_date = request.POST.get('endDate')
        if start_date == end_date:
            orders = OrderProduct.objects.all().filter(order__created_at__date=start_date)
            msg = 'Showing the results of the date : '+ start_date
            
        else:
            orders = OrderProduct.objects.all().filter(order__created_at__range=[start_date,end_date])
            msg = 'Showing the results between '+ start_date + '--' + end_date

    context = {
        'orders':orders,
        'msg':msg,
    }
    return render(request, 'admin_temp/sales_report.html', context)

def yearly_sales(request):
    if request.method == 'POST':
        print('request.post ',request.POST)
        year = request.POST.get('selectedYear')
        print('year : ',year)
        orders = Order.objects.all().filter(created_at__year=year)
        if orders.count() == 0:
            msg = 'No result found for ' + year
        else:
            msg = 'The details of sales in ' + year + ' are :'
        context = {
            'msg':msg,
            'orders':orders,
        }
    return render(request, 'admin_temp/sales_report.html', context)

def monthly_sales(request):
    print('request.post : ', request.POST)
    month = request.POST.get('month')
    orders = Order.objects.all().filter(created_at__month=month)
    if orders.count() == 0:
        msg = 'No result found for this month'
    else:
        msg = 'The details of the sales in this month are : '
    context = {
        'msg':msg,
        'orders':orders,
    }
    return render(request, 'admin_temp/sales_report.html', context)

def accept_return_request(request, id):
    try:
        order = Order.objects.get(pk=id)
        if order.status == 'accepted':
            
            
            # Calculate the refund amount (adjust this calculation according to your requirements)
            refund_amount = 0.5 * order.order_total  # Example: refunding 50% of the order total

            # Get the user associated with the order
            user = order.user

            # Get or create the user's wallet
            wallet, created = Wallet.objects.get_or_create(user=user)

            # Add the refund amount to the user's wallet balance
            wallet.balance += refund_amount
            wallet.save()

            # Create a transaction record to track the refund
            transaction = Transaction.objects.create(
                user=user,
                amount=refund_amount,
                description='Refund for Order #{}'.format(order.order_number)
            )

            # Update the order status to reflect that the return request has been accepted
            order.status = 'accepted'
            order.save()

            return redirect('admin_dashboard')  # Redirect to the admin dashboard or a success page
        else:
            # Handle the case where the order status is not 'Return Requested'
            return redirect('admin_dashboard')
    except Order.DoesNotExist:
        # Handle the case where the order doesn't exist
        return redirect('admin_error_page')