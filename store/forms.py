from django import forms
from .models import product,Size,coupon


class Productform(forms.ModelForm):
    class Meta:
        model = product
        fields = ('product_name','size','description','prize','offer_price','images','category','stock')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add Bootstrap form-control class to each field widget
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['class'] = 'form-control'

        self.fields['category'].empty_label = 'Select Catgory'
        self.fields['size'].empty_label = 'Select size '

class SizeForm(forms.ModelForm):
    class Meta:
        model = Size
        fields =('size',)
        
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['size'].widget.attrs['class'] = 'form-control'

class CouponForm(forms.ModelForm):
    class Meta:
        model = coupon
        fields =('coupon_code','is_expired','discount_price','minimum_amount',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['coupon_code'].widget.attrs['class'] = 'form-control'
        self.fields['discount_price'].widget.attrs['class'] = 'form-control'
        self.fields['minimum_amount'].widget.attrs['class'] = 'form-control'