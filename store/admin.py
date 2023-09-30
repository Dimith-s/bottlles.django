from django.contrib import admin
from .models import product,ProductImage,Size,coupon

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name','prize','offer_price','stock','category','modified_date','is_available')
    prepopulated_fields = {'slug':('product_name',)}

admin.site.register(product,ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(Size)
admin.site.register(coupon)