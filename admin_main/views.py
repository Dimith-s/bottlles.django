from django.shortcuts import render,redirect
from accounts.models import Accounts
from store.models import product,ProductImage
from category.models import category
from django.http import JsonResponse
from store.forms import Productform
from category.forms import Categoryform

# Create your views here.
def home(request):
    return render(request,'admin_temp/adminhome.html')



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
                product = form.save()
                if request.FILES.get('pr_images') != 0:
                    images = request.FILES.getlist('pr_images')
                    for img in images:
                        image = ProductImage.objects.create(product=product, image=img)
                        image.save()
                form.save()
                return redirect('productlist')
            else:
                print('form not valid')
                print(form.errors)
        form = Productform()
    else:
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


