from django.contrib import admin
from .models import *

# Register your models here.
class ItemInline(admin.TabularInline):
    model = Item
    min_num = 1
    raw_id_fields = ('category',)

@admin.register(Category)
class Category(admin.ModelAdmin):
    list_display = ['category',]
    inlines = (ItemInline,)

class CartItemInline(admin.TabularInline):
    model = CartItem
    min_num = 1
    raw_id_fields = ('item',)

@admin.register(Cart)
class Cart(admin.ModelAdmin):
    list_display = ['user','total','count']
    inlines = (CartItemInline,)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id','billing_address','status','transaction_id','amount',]
    list_editable = ['status',]
