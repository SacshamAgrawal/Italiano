from django.core.management.base import BaseCommand
from io import BytesIO
from django.core.files.images import ImageFile
from pizza.models import *
from PIL import Image
import os
import logging
from collections import Counter

logger = logging.getLogger(__name__)

# Files folder
source_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))),'Files/pizza/images')

class Command(BaseCommand):
    help = 'Import menu for the Italiano'
    
    def handle(self, *args, **kwargs):
        self.stdout.write("Importing Menu")
        c=Counter()

        # Adding pizza items
        pizza,created_cat = Category.objects.update_or_create(category = 'Pizza')
        pizza.save();
        # logger.debug("Pizzas Category : " +str(created_cat))
        if created_cat:
            c["Category Created"]+=1;

        pizza_folder = os.path.join(source_folder,'pizza') 
        for file in os.listdir(pizza_folder):
            name = None
            with open( os.path.join(pizza_folder,file),'rb' ) as f:
                name = file.split('.')[0]
                image = ImageFile(f,name=file)
                # logger.debug("Adding File name : "+str(file))
                pizza_item ,created = Item.objects.update_or_create( defaults = {'image':image ,'category':pizza} , name = name )
                pizza_item.save();
                if created:
                    c["Pizzas Created"]+=1
                    logger.debug("Adding to the Menu - "+str(file) )

         # Adding drinks items
        drinks,created_cat = Category.objects.update_or_create(category = 'Drinks')
        drinks.save();
        # logger.debug("DRinks Category : " +str(created_cat))
        if created_cat:
            c["Category Created"]+=1;

        drinks_folder = os.path.join(source_folder,'drinks') 
        for file in os.listdir(drinks_folder):
            name = None
            with open( os.path.join(drinks_folder,file),'rb' ) as f:
                name = file.split('.')[0]
                image = ImageFile(f,name=file)
                drinks_item , created = Item.objects.update_or_create( defaults = {'image':image ,'category':drinks} , name = name )
                drinks_item.save();
                if created:
                    c["Drinks Created"]+=1
                    logger.debug("Adding to the Menu - "+str(file) )

         # Adding burgers items
        burger,created_cat = Category.objects.update_or_create(category = 'Burger')
        burger.save();
        # logger.debug("burgers Category : " +str(created_cat))
        if created_cat:
            c["Category Created"]+=1;

        burger_folder = os.path.join(source_folder,'burgers') 
        for file in os.listdir(burger_folder):
            name = None
            with open( os.path.join(burger_folder,file),'rb' ) as f:
                name = file.split('.')[0]
                image = ImageFile(f,name=file)
                burger_item , created = Item.objects.update_or_create( defaults = {'image':image ,'category':burger} , name = name )
                burger_item.save();
                if created:
                    c["Burgers Created"]+=1
                    logger.debug("Adding to the Menu - "+str(file) )

         # Adding pasta items
        pasta,created_cat = Category.objects.update_or_create(category = 'Pasta')
        pasta.save();
        # logger.debug("pastas Category : " +str(created_cat))
        if created_cat:
            c["Category Created"]+=1;

        pasta_folder = os.path.join(source_folder,'pasta') 
        for file in os.listdir(pasta_folder):
            name = None
            with open( os.path.join(pasta_folder,file),'rb' ) as f:
                name = file.split('.')[0]
                image = ImageFile(f,name=file)
                pasta_item , created = Item.objects.update_or_create( defaults = {'image':image ,'category':pasta} , name = name )
                pasta_item.save()
                if created:
                    c["Pasta Created"]+=1
                    logger.debug("Adding to the Menu - "+str(file) )

        self.stdout.write("No of Categories Created : " + str(c["Category Created"]))

        #Importing Chefs Data
        chef_folder = os.path.join(source_folder,'Chefs')
        for file in os.listdir(chef_folder):
            with open(os.path.join(chef_folder,file),'rb') as f:
                name = file.split('.')[0]
                image = ImageFile(f,name = file)
                chef , created = Chef.objects.get_or_create(name = name, display_picture = image)
                if created :
                    c["Chefs Created"]+=1
                    chef.save()
                
        logger.debug("No of Added Chefs :" + str(c["Chefs Created"]))
