from django import forms
from .models import *

class AddressForm(forms.ModelForm):
    
    class Meta:
        model = Address
        fields = ("address1","address2","zip_code","city","country",)
