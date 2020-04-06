from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import UsernameField
from allauth.account.forms import SignupForm , LoginForm
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.formfields import PhoneNumberField

class CustomUserCreationForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ('email',"mobile_number")
        field_classes = {"email":UsernameField }

class  CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = UserChangeForm.Meta.fields

class CustomSignupForm(SignupForm):

    field_order = [
        'mobile_number',
        'email',
        "password1",
        "password2",
    ]

    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        self.fields['mobile_number'] = PhoneNumberField()

    def save(self, request):
        user = super(CustomSignupForm,self).save(request)
        mobile_number = self.cleaned_data.get('mobile_number')
        if mobile_number:
            user.mobile_number = mobile_number
        user.save()
        return user