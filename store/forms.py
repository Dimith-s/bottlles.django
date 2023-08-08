from django import forms
from .models import product


class Productform(forms.ModelForm):
    class Meta:
        model = product
        fields = ('product_name','description','prize','images','category','stock')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add Bootstrap form-control class to each field widget
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['class'] = 'form-control'

        self.fields['category'].empty_label = 'Select Catgory'