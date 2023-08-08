from django import forms
from .models import Accounts

class registrationform(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'enter password',
        'class' : 'form-group',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'confirm password',
        
    }))
    class Meta:
        model = Accounts
        fields = ['first_name','last_name','phone_number','email','password']

    def clean(self):
        cleaned_data = super(registrationform,self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "password does not match"
            )

    def __init__(self,*args,**kwargs):
        super(registrationform,self).__init__(*args,**kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'enter the first name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'enter the last name'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'enter the phone number'
        self.fields['email'].widget.attrs['placeholder'] = 'enter the email'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-group'



from django import forms

class VerifyForm(forms.Form):
    # Define your form fields here
    code = forms.CharField(max_length=6)



class VerifyForm(forms.Form):
    code = forms.CharField(max_length=8, required=True, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Code'}))