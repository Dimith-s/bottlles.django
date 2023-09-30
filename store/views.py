from django.shortcuts import render,get_object_or_404
from .models import product,Size
from category.models import category
from carts.views import _cart_id
from carts.models import cartitem
from django.http import HttpResponse
from django.db.models import Q
from orders.models import OrderProduct,Order

# Create your views here.
def store(request,category_slug=None):
    print("requested")
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(category,slug = category_slug)
        print("************")
        print(categories)
        products = product.objects.filter(category = categories,is_available=True)
        print(products)
        product_count = products.count()
    else:
        products = product.objects.filter(category = categories,is_available=True)
        print(products)
        product_count = products.count()

    products = product.objects.all().filter(is_available=True)
    product_count = products.count()

    context = {
        'products': products,
        'product_count': product_count,
        
    }
    return render(request,'store/store.html',context)

def product_detail(request,category_slug,product_slug):
    try:
        single_product = product.objects.get(category__slug=category_slug, slug = product_slug)
        if request.user.is_authenticated:
            in_cart = cartitem.objects.filter(user=request.user,product=single_product).exists()   
        else:
            in_cart = cartitem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()
        sizes = Size.objects.filter(product=single_product)

    except Exception as e:
        raise e
    print('single_product : ', single_product)
    context = {
        'single_product': single_product,
        'in_cart': in_cart,
        'sizes': sizes,
    }
    return render(request,'store/product_detail.html', context)


def search(request):
    
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        print("keyword:",keyword)
        if keyword:
            Products = product.objects.order_by("-created_date").filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            print(Products)
            product_count = Products.count()

    context ={
        'products':Products,
        'product_count': product_count,
    }
    return render(request,'store/store.html',context)

def invoice(request, order_item_id):
    print('orderitem id : ', order_item_id)
    ordered_product = Order.objects.get(id=order_item_id, user=request.user)
    orderproducts = OrderProduct.objects.filter(order=ordered_product)
   
    context = {
        'items':orderproducts,
        
        'item': ordered_product,
    }
    print(orderproducts)
    return render(request,'orderr/invoice.html',context)

#download invoice

from io import BytesIO
from xhtml2pdf import pisa
from django.views.generic import View
from django.template.loader import get_template



class generateInvoice(View):

    def get(self, request, orderitem_id, *args, **kwargs):
        try:
            orderproduct = Order.objects.get(id=orderitem_id)
        except:
            return HttpResponse('505 not found')
        context = {
            'item':orderproduct,
            'discount':0,
        }
        
        pdf = render_to_pdf('printinvoice.html',context)
        return HttpResponse(pdf, content_type='application/pdf')
    
def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None