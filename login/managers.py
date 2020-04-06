from django.contrib.auth.models import BaseUserManager
from django.utils.translation import ugettext_lazy as _

class UserManager(BaseUserManager):
    use_in_migrations = True
    
    def _create_user(self , email, mobile_number,password,**extra_fields):
        if not email:
            raise ValueError(_("The email must be provided"))
        if not mobile_number:
            raise ValueError(_("The mobile number should be provided"))
        email = self.normalize_email(email)
        user = self.model(email = email, mobile_number = mobile_number, **extra_fields)
        user.set_password(password)
        user.save(using = self._db)
        user.full_name = str(user.first_name)+" "+str(user.last_name)
        return user 

    def create_user(self,email,mobile_number,password = None , **extra_fields):
        extra_fields.setdefault("is_staff",False)
        extra_fields.setdefault("is_superuser",False)
        return self._create_user(email,mobile_number,password,**extra_fields)

    def create_superuser(self,email,mobile_number,password=None, **extra_fields):
        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_superuser",True) 
        extra_fields.setdefault("is_active",True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_("is_staff must be set true for superuser"))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_("is_superuser must be set true for superuser"))
        return self._create_user(email,mobile_number,password,**extra_fields)
