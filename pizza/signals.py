from django.contrib.auth.signals import user_logged_in
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from .models import *

from pprint import pprint

@receiver(user_logged_in)
def merge_cart_if_found(sender, user, request, **kwargs):
    logger.debug("Signal Fired...")
    pprint(request)
    pprint(user)
    cart = getattr(request,'cart',None)
    if cart:
        logger.debug("Cart aldready exists. :)")
        try:
            user_cart = Cart.objects.get(user = user)
            for cartitem in cart.cartitem.all() :
                new_cartitem , created = CartItem.objects.update_or_create(cart = user_cart, item = cartitem.item)
                new_cartitem.quantity = cartitem.quantity
                new_cartitem.save() 
                logger.debug('Cart deleted with Cart_id ='+str(cart.id))
                cart.delete()
                request.cart = user_cart
                request.session['cart_id'] = user_cart.id
                logger.debug("Cart Merged.....")
        except Cart.DoesNotExist:
            cart.user = user
            cart.save()
            request.cart = cart
            request.session['cart_id'] = cart.id
            logger.debug("Cart Copied ... cart id ="+str(cart.id))
    
    else:
        logger.debug("Cart Doesn't Exist")