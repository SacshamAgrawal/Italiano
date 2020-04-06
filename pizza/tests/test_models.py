from django.test import TestCase,override_settings
from django.contrib.auth import get_user_model
from pizza.models import *
from pizza.forms import *
from django.core.files.images import ImageFile
import tempfile

# from PIL import ImageFile, Image
import os
from io import BytesIO

User = get_user_model()

@override_settings(MEDIA_ROOT = 'test_files/test_media',MEDIA_URL='/test_files/test_media/')    
class TestModels(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            email = 'sacshamagrawal28@gmail.com',
            mobile_number = '1234567890',
            password = 'abcdefgh28',  
        )
    def test_all_models(self):
        
        category = Category.objects.create(
            category = 'category1'
        )       
        with open(os.path.join(os.getcwd(),'test_files/test_static/item1.jpg'),'rb') as f:
            image = ImageFile(f,name = 'item1.jpg')
            item1 = Item.objects.create(
                category = category,
                name = 'item1',
                image = image,
                price = '34.34',
            )
        self.assertEqual(item1.image_thumbnail.name,str('item-thumbnails/')+str(item1.image.name))
        
        with open(os.path.join(os.getcwd(),'test_files/test_static/item2.jpg'),'rb') as f:
            image = ImageFile(f,name = 'item2.jpg')
            item2 = Item.objects.create(
                category = category,
                name = 'item2',
                image = image,
                price = '10',
            )
        self.assertEqual(item2.image_thumbnail.name,str('item-thumbnails/')+str(item2.image.name))
        
        cart = Cart.objects.create(
            user = self.user
        )
        
        self.assertEqual(len(category.items.all()),2)
        cartitem1 = CartItem.objects.create(
            cart = cart,
            item = item1,
        )
        cartitem2 = CartItem.objects.create(
            cart = cart,
            item = item2,
            quantity = 4,
        )
        
        self.assertEqual(len(cart.cartitem.all()),2)
        self.assertEqual(cart.count(),5)
        self.assertEqual(cart.total(),74.34)
