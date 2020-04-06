from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from .managers import UserManager
from phonenumber_field.modelfields import PhoneNumberField

class User(AbstractUser):
    
    email = models.EmailField( max_length=254 , unique=True)
    mobile_number = PhoneNumberField()
    full_name = models.CharField(_("Full Name"), max_length=50)
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ["mobile_number",]

    def __str__(self):
        return self.email
    
    objects = UserManager()

