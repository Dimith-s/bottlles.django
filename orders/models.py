from django.db import models
from accounts.models import Accounts, Address
from store.models import product

# Create your models here.

class Payment(models.Model):
    user = models.ForeignKey(Accounts,on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.payment_method
    

class Order(models.Model):
    STATUS = (
        ('New','New'),
        ('Accepted','Accepted'),
        ('Completed','Completed'),
        ('Cancelled','Cancelled'),
    )


    user = models.ForeignKey(Accounts,on_delete=models.SET_NULL,null=True)
    payment = models.ForeignKey(Payment,on_delete=models.SET_NULL,blank=True,null=True)
    order_number = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255,null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    order_note = models.CharField(max_length=100,blank=True,null=True)
    order_total = models.FloatField()
    tax = models.FloatField(null=True)
    status = models.CharField(max_length=10,choices=STATUS,default='New')
    ip = models.CharField(blank=True,max_length=20)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.user.first_name

    def full_name(self):
        return self.first_name + self.last_name
    
choices = {
    ('Order Placed', 'Order Placed'),
    ('shipped', 'shipped'),
    ('out for delivery','out for delivery'),
    ('delivered','delivered'),
    ('cancelled','cancelled'),
}
        
class OrderProduct(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    Payment = models.ForeignKey(Payment,on_delete=models.SET_NULL,blank=True,null=True)
    # user = models.ForeignKey(Accounts,on_delete=models.CASCADE)
    Product = models.ForeignKey(product,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    product_price = models.CharField()
    status = models.CharField(max_length=100,choices=choices,default='Order Placed')
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.Product.product_name
    


 