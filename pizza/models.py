from django.db import models
from django.utils.translation import ugettext_lazy as _
from PIL import Image,ImageOps
import logging
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.contrib.auth import get_user_model
from datetime import datetime

THUMNAIL_SIZE = (70,70)
USER = get_user_model()
logger = logging.getLogger(__name__)

# Create your models here.

class Category(models.Model):
    """Model definition for Category."""

    category = models.CharField(_("Category Name"),max_length= 32)    

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.category

class Item(models.Model):
    """Model definition for Item."""

    category = models.ForeignKey(Category, on_delete=models.CASCADE , related_name='items')
    name = models.CharField(_("Item Name"), max_length=50)
    description = models.TextField(_("Item Discription"),default="Will Be Added..")
    image = models.ImageField(_("Item Image"), upload_to="item-images")
    image_thumbnail = models.ImageField(_("Item Thumbnail"),upload_to="item-thumbnails",blank=True, null=True)
    price = models.DecimalField(decimal_places=2,default = 20.43,max_digits=7)

    class Meta:
        """Meta definition for Item."""

        verbose_name = 'Item'
        verbose_name_plural = 'Items'

    def __str__(self):
        return self.name

    def save(self,*args, **kwargs):
   
        super(Item,self).save(*args, **kwargs)
        if str(self.image_thumbnail) is "":
        
            try:
                img = Image.open(default_storage.open(self.image.name))
            except:
                raise ValueError("Image file not openning for thumbnail creation...")
                        
            img.thumbnail(THUMNAIL_SIZE,Image.ANTIALIAS )  
            img = ImageOps.fit(img,THUMNAIL_SIZE,Image.ANTIALIAS)             
            temp_thumb = BytesIO()
            img.save(temp_thumb,"JPEG")
            temp_thumb.seek(0)

            self.image_thumbnail.save(self.image.name , ContentFile(temp_thumb.read()) ,save = False ) 
            temp_thumb.close()
            logger.info("Thumbnail Generated as "+str( self.image_thumbnail.name ))

class Cart(models.Model):

    user = models.ForeignKey(USER,on_delete=models.CASCADE, blank=True,null = True , related_name="cart" )

    def total(self):
        return float(sum([cartitem.quantity * cartitem.item.price for cartitem in self.cartitem.all()]))
    
    def count(self):
        count =  int(sum([cartitem.quantity for cartitem in self.cartitem.all()]))
        return count 

    def is_empty(self):
        return (self.count() == 0)

    class Meta:
        verbose_name = _("cart")
        verbose_name_plural = _("carts")

    def __str__(self):
        return str(self.id)

class CartItem(models.Model):

    cart = models.ForeignKey(Cart , on_delete = models.CASCADE , related_name='cartitem')
    item = models.ForeignKey(Item,on_delete = models.CASCADE)
    quantity = models.PositiveIntegerField(_("quantity"),default = 1)

    class Meta:
        verbose_name = _("CartItem")
        verbose_name_plural = _("CartItems")

    def __str__(self):
        return str(self.item.name)

class Address(models.Model):

    SUPPORTED_COUNTRIES = (
        ('IN',"INDIA"),
    )
    user = models.ForeignKey(USER, on_delete=models.CASCADE , related_name='addresses')
    name = models.CharField(max_length=32,null=True)
    address1 = models.CharField("Address line 1", max_length=128,null=True)
    address2 = models.CharField(
        "Address line 2", max_length=128, null=True
    )
    zip_code = models.IntegerField(
        "ZIP / Postal code",null=True,
    )
    city = models.CharField(max_length=32,null=True)
    country = models.CharField(
        max_length=3, choices=SUPPORTED_COUNTRIES , default='IN'
    )
    def __str__(self):
        return ", ".join(
            [
                 self.name,
                 self.address1,
                 self.address2,
                 str(self.zip_code),
                 self.city,
                 self.country,
            ]
       )

    class Meta:
        verbose_name = _("address")
        verbose_name_plural = _("addresses")

class Order(models.Model):

    STATUS = (
        (1,"NEW"),
        (2,"PAID"),
        (3,"PROCESSING"),
        (4,"SENT_FOR_DELIVERY"),
        (5,"COMPLETED"),
    )

    user = models.ForeignKey( USER , on_delete=models.SET_NULL , blank=True, null = True , related_name='orders')
    order_id = models.CharField(_("ORDER_ID"),null=True,max_length=13)
    billing_address = models.CharField(_("Billing Address"),max_length=128)
    status = models.IntegerField(_("STATUS OF ORDER"),choices=STATUS,default = 1)
    transaction_id = models.CharField(_("TRANSACTION ID"), max_length=50, blank = True)
    amount = models.DecimalField(_("AMOUNT "),default= 0 ,max_digits=8 , decimal_places=2)
    time_of_order = models.TimeField(auto_now=True)
    last_spoken_to = models.ForeignKey(USER,on_delete = models.SET_NULL,null = True, related_name='cs_chat')

    def save(self,*args, **kwargs):
        super(Order,self).save(*args, **kwargs)
        self.order_id = str("ITALIANO"+format(self.id,'05d'))
    
    def __str__(self):
        return " ".join(
            [
                str(self.user),
                self.order_id,
                self.billing_address,
                self.transaction_id,
                str(self.amount),
            ]
       )

    class Meta:
        verbose_name = _("order")
        verbose_name_plural = _("orders")    

class OrderItem(models.Model):

    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='orderitem')
    item = models.ForeignKey(Item,on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default = 1)

    class Meta:
        verbose_name = _("OrderItem")
        verbose_name_plural = _("OrderItems")

    def __str__(self):
        return self.name

class Chef(models.Model):

    name = models.CharField(_("Chef's Name"), max_length=32)
    speciality = models.CharField(_("Speciality"), max_length=16 , default="Chef")
    bio = models.TextField(_("Chef's Bio"), max_length = 80, default= "Cooking is an art.")
    display_picture = models.ImageField(_("Chefs DP"), upload_to="Chefs", default='default_chef.jpg')

    class Meta:
        verbose_name = _("chef")
        verbose_name_plural = _("chefs")

    def __str__(self):
        return self.name