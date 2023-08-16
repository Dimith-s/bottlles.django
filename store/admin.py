from django.contrib import admin
from .models import product,ProductImage

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name','prize','stock','category','modified_date','is_available')
    prepopulated_fields = {'slug':('product_name',)}

admin.site.register(product,ProductAdmin)
admin.site.register(ProductImage)