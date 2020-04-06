from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class TestUserModel(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            full_name = 'Sacsham Agrawal',
            first_name = 'Sacsham',
            last_name = 'Agrawal',
            email = 'sacshamagrawal28@gmail.com',
            mobile_number = '8840353310',
            password = 'abcd',
        )

    def test_user_model_creation(self):
        user1 = User.objects.get(email = 'sacshamagrawal28@gmail.com')
        self.assertEqual(self.user,user1)
        self.assertEqual(self.user.first_name,'Sacsham')
        self.assertEqual(self.user.full_name,'Sacsham Agrawal')
    
    