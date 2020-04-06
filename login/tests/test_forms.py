from django.test import TestCase
from login.forms import *

class TestLoginForms(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.valid_form = CustomUserCreationForm({
            'mobile_number': '8840353310',
            'email' : 'sacshamagrawal28@gmail.com',
            'password1' : 'abcdefgg23@',
            'password2' : 'abcdefgg23@',
            'first_name' : 'Sacsham',
            'last_name' : 'Agrawal',
        })
        cls.invalid_form = CustomUserCreationForm({
            'mobile_number': '8840353310',
            'email' : 'sacshamagrawal28@gmail.com',
            'password1' : 'abcd',
            # 'password2' : 'abcd',
            'first_name' : 'Sacsham',
            'last_name' : 'Agrawal',
        })
    
    def test_userCreationForm(self):
        self.assertTrue(self.valid_form.is_valid())
        self.assertFalse(self.invalid_form.is_valid())
        user = self.valid_form.save()
        self.assertEqual(str(user),'sacshamagrawal28@gmail.com')
        
    def test_authentication(self):
        self.valid_form.save()
        self.assertTrue(self.client.login(
            email='sacshamagrawal28@gmail.com', password = 'abcdefgg23@'
        ))
