from django.test import TestCase,override_settings
from django.test import Client
from django.contrib.auth import get_user_model , authenticate , login
from pizza.models import *
from pizza.forms import *
from django.core.files.images import ImageFile
import tempfile
from django.shortcuts import reverse
from django.contrib import auth
from django.conf import settings
from allauth.account.utils import perform_login

# from PIL import ImageFile, Image
import os
from io import BytesIO
from pprint import pprint

User = get_user_model()

@override_settings(MEDIA_ROOT = 'test_files/test_media',MEDIA_URL='/test_files/test_media/')    
class TestSignals(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            email = 'sacshamagrawal28@gmail.com',
            mobile_number = '1234567890',
        )
        cls.user.set_password('abcdefgh28')
        cls.user.save()

    def test_signals(self):
        
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
        self.assertEqual(len(category.items.all()),2)
        
        response = self.client.get(reverse('add_to_cart'),{'item_id':item1.id})
        self.assertEqual(response.status_code,200)
        response = self.client.get(reverse('add_to_cart'),{'item_id':item2.id})
        self.assertEqual(response.status_code,200)
        response = self.client.get(reverse('menu'))
        self.assertEqual(response.status_code,200)

        cart = response.wsgi_request.cart
        self.assertEqual(len(cart.cartitem.all()),2)
        self.assertIsNone(cart.user)
        self.assertEqual(self.client.session['cart_id'],cart.id)
        self.assertEqual(cart.count(),2)
        
        # testing signup form
        response = self.client.post(reverse('account_signup'),{
            'email':'sac@123.com',
            'mobile_number':'1234567890',
            'password1':'chotu12345',
            'password2':'chotu12345',
        },follow = True)
        self.assertEqual(len(User.objects.all()),2)
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        cart.refresh_from_db()
        self.assertEqual(cart.user,auth.get_user(self.client))
        self.client.logout()
        # response = self.client.get(reverse('menu'))
        # self.assertEqual(response.status_code,200)
        self.assertTrue(auth.get_user(self.client).is_anonymous)
        print(Cart.objects.all().values())
        
        response = self.client.get(reverse('add_to_cart'),{'item_id':item1.id})
        self.assertEqual(response.status_code,200)
        response = self.client.get(reverse('add_to_cart'),{'item_id':item2.id})
        self.assertEqual(response.status_code,200)
        # response = self.client.trace(reverse('menu'))
        # print(Cart.objects.all().values())

        # testing login form        
        user = authenticate(response.wsgi_request,email='sac@123.com', password='chotu12345')
        pprint(Cart.objects.get(user=user))
        pprint(dict(self.client.session))
        self.assertTrue(self.client.login(email='sac@123.com', password='chotu12345'))
        response = self.client.trace(reverse('menu'))
        self.assertEqual(response.status_code,200)
        print(auth.get_user(self.client).id)
        # self.assertTrue(auth.get_user(self.client).is_authenticated)
        self.assertTemplateUsed('index.html')
        cart = response.wsgi_request.cart
        print(Cart.objects.all().values())
        