from django import forms
from .models import category

class Categoryform(forms.ModelForm):
    class Meta:
        model = category
        fields = ('category_name','cat_image','discription')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        # Add Bootstrap form-control class to each field widget
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['class'] = 'form-control'

        