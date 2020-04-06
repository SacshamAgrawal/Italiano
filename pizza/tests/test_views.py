from django.test import TestCase
from django.shortcuts import reverse
from pizza.models import *
from django.contrib.auth import get_user_model
from pizza.forms import *

User = get_user_model()

class TestPage(TestCase):
    def test_homepage_works(self):

        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'pizza/index.html')
        