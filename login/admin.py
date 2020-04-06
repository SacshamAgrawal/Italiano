from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import User
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.utils.translation import ugettext_lazy as _

class CustomUserAdmin(UserAdmin):
    model = User
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
        
    fieldsets = (
        (
            _("Credentials User"),
            {"fields": ("email","mobile_number","password",)}),
        (
            _("Personal info"),
            {"fields":('first_name',"last_name","full_name")},
        ),
        (
            _("Permissions"),
            {"fields":("is_active","is_staff","is_superuser","groups","user_permissions")},
        ),
        (
            _("Important dates"),
            {"fields":("last_login","date_joined")},
        ),
    )
    add_fieldsets = (
        (None,{
            "classes":("wide",),
            "fields":("email",'first_name',"last_name","mobile_number","password1","password2",),
        }),
    )
    list_display = (
        "email",
        "first_name",
        "last_name",
        "mobile_number",
        "is_staff",
    )    
    search_fields = (
        "email",
        "first_name",
        "mobile_number",
    )
    ordering=("email",)

# Register your models here.
admin.site.register(User,CustomUserAdmin)
