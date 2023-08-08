from django.shortcuts import render
from store.models import product
from django.views.decorators.cache import never_cache
from category.models import category



@never_cache
def home(request):
    categories = category.objects.filter(is_available=True)
    products = product.objects.all().filter(is_available=True,category__in=categories)
    print('products : ', products)
    context = {
        'products': products,
    }
    return render (request,'home.html',context) 