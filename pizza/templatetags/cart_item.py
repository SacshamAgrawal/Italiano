from django import template
import logging
from pprint import pprint

logger = logging.getLogger(__name__)

register = template.Library()

@register.inclusion_tag('pizza/cart_item.html')
def get_cart_item(cart,user):
    # logger.debug("Loading Ajax Cart....")
    context = {
        'total':'0.00',
        'no_of_items':0,
    }
    if not cart or cart.is_empty():
        context['cart_items']=None
    else:
        context['total'] = cart.total()
        context['no_of_items'] = cart.count()
        context['cart_items'] = [cartitem for cartitem in cart.cartitem.all()]
    
    context['user']=user
    return context

@register.inclusion_tag('pizza/address.html')
def get_shipping_address_form():
    pass