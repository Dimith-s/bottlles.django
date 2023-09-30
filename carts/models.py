from django.db import models
from store.models import product
from accounts.models import Accounts
from store.models import coupon

# Create your models here.
class cart(models.Model):
    cart_id = models.CharField(max_length=250,blank=True)
    
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id
class cartitem(models.Model):
    user = models.ForeignKey(Accounts,on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(product,on_delete=models.CASCADE)
    cart = models.ForeignKey(cart,on_delete=models.CASCADE,null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.original_price() * self.quantity

    def __str__(self) -> str:
        return str(self.product)

