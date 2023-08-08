from django.db import models
from django.urls import reverse

# Create your models here.
class category(models.Model):
    category_name = models.CharField(max_length=50,unique=True)
    slug = models.SlugField(max_length=100,unique=True)
    discription = models.TextField(max_length=255,blank=True)
    cat_image = models.ImageField(upload_to='photos/categories',blank=True)
    is_available = models.BooleanField(default=False)


    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_url(self):
        return reverse('products_by_category',args=[self.slug])

    def __str__(self) -> str:
        return self.category_name