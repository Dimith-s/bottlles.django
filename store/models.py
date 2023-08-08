from django.db import models
from category.models import category
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.
class product(models.Model):
    product_name = models.CharField(max_length=200,unique=True)
    slug         = models.SlugField(max_length=200,unique=True)
    description  = models.TextField(max_length=500,blank=True)
    prize        = models.IntegerField()
    images       = models.ImageField(upload_to='photos/product')
    stock        = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category     = models.ForeignKey(category,on_delete=models.CASCADE) 
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date= models.DateTimeField(auto_now=True)


    def get_url(self):
        return reverse('product_detail',args = [self.category.slug,self.slug])

    def __str__(self) -> str:
        return self.product_name
    
    def save(self, *args, **kwargs):
        # Generate the slug from the product name
        self.slug = slugify(self.product_name)
        super(product, self).save(*args, **kwargs)
