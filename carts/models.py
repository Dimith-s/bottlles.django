from django.db import models
from store.models import product

# Create your models here.
class cart(models.Model):
    cart_id = models.CharField(max_length=250,blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id
class cartitem(models.Model):
    product = models.ForeignKey(product,on_delete=models.CASCADE)
    cart = models.ForeignKey(cart,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.prize * self.quantity

    def __str__(self) -> str:
        return self.product

