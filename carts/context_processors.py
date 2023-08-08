from .models import cart,cartitem
from .views import _cart_id

def counter(request,cart_count = 0):
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart_model = cart.objects.filter(cart_id = _cart_id(request))
            cart_items = cartitem.objects.all().filter(cart=cart_model[:1])

            for cart_item in cart_items:
                cart_count  += cart_item.quantity

        except cart.DoesNotExist:
            cart_count = 0

    return dict(cart_count=cart_count)
