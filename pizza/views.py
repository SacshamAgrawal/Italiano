from django.shortcuts import render, get_object_or_404 , redirect ,reverse ,HttpResponse
from .models import *
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from paytm import Checksum
from .forms import *
from .serializers import *

# for debugging
from pprint import pprint
import logging
import os

# for rest framework
from rest_framework import viewsets , authentication,permissions

# merchant key ( keep it a secret )
MERCHANT_ID = os.environ.get('PAYTM_MERCHANT_ID')
MERCHANT_KEY = os.environ.get('PAYTM_MERCHANT_KEY')

USER = get_user_model()
logger = logging.getLogger(__name__)

# Class Based Views

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()        

# Function Based Views

def homepage(request):
    pizza_list = Item.objects.filter(category__category = 'Pizza').values()
    pizza_items = [pizza for pizza in pizza_list ]
    chefs = Chef.objects.all()
    return render(request,'pizza/index.html',{'pizza_items':pizza_items,'chefs':chefs})

def menu(request):

    pizza_list = Item.objects.filter(category__category = 'Pizza').values()
    pizza_items = [pizza for pizza in pizza_list ]
    drink_list = Item.objects.filter(category__category = 'Drinks').values()
    drink_items = [drink for drink in drink_list]
    burger_list = Item.objects.filter(category__category = 'Burger').values()
    burger_items = [burger for burger in burger_list]
    pasta_list = Item.objects.filter(category__category = 'Pasta').values()
    pasta_items = [pasta for pasta in pasta_list]

    count = {
        'pizza':len(pizza_items),
        'burger':len(burger_items),
        'drinks':len(drink_items),
        'pasta':len(pasta_items),
    }
    context = {
        'pizza_items':pizza_items,
        'drinks_items':drink_items,
        'burger_items':burger_items,
        'pasta_items':pasta_items,
        'count':count,
    }
    response =  render(request,'pizza/menu.html',context=context)
    # pprint(response)
    return response

def add_to_cart(request):
    
    try:
        if( Order.objects.filter(user = request.user).filter(order_status__gt=1).count() ):
            return redirect('homepage')
    except:
        logger.debug("Never try anything rubbish.....")

    if 'cart_id' not in request.session :
        if request.user.is_authenticated:
            user = request.user
        else:
            user = None        

        cart = Cart.objects.create(user = user )
        request.session['cart_id'] = cart.id
        request.cart = cart
        logger.debug('Cart Created with Cart_id ='+str(cart.id))
    
    cart = request.cart
    
    try:
        item = get_object_or_404(Item, id = request.GET.get('item_id') )
    except:
        logger.debug("Item Not Found while adding to Cart..")
    
    cartitem , created = CartItem.objects.get_or_create(cart = cart , item = item )
    if created:
        logger.debug("Item created in the cart :"+str(item))
    if not created:
        cartitem.quantity += 1 
        cartitem.save()
    
    return render(request,'pizza/cart_refresh.html')

@login_required
def checkout(request):
    
    logger.info("Checking Out.....")
    active_user = request.user 
    
    address , created = Address.objects.get_or_create(user = active_user)        
    addressform = AddressForm(request.POST,instance=address)
    logger.error(addressform.errors)
    if addressform.is_valid():
        # address = addressform.save(commit=False)
        address.name = str(request.POST['firstname']) + " " + str(request.POST['lastname'])  
        address.save()
    
    else:
        address.delete()
        logger.debug("Form is not valid...")
        return redirect('homepage')
    
    order = Order.objects.create(user = active_user, amount = str(request.cart.total()) )    
    order.billing_address = str(address)
    order.save()

    paytmParams = {
        "MID" : MERCHANT_ID,
        "WEBSITE" : "WEBSTAGING",
        "INDUSTRY_TYPE_ID" : "Retail",
        "CHANNEL_ID" : "WEB",
        "ORDER_ID" : str(order.order_id),
        "CUST_ID" : active_user.email,
        "EMAIL" : active_user.email,
        "TXN_AMOUNT" : "{0:.2f}".format(float(order.amount)),
        "CALLBACK_URL" : "http://localhost:8000/orderdone/",
    }
    if active_user.mobile_number :
        paytmParams['MOBILE_NO'] = str( active_user.mobile_number )

    checksum = Checksum.generate_checksum(paytmParams, MERCHANT_KEY)
    paytmParams["CHECKSUMHASH"] = checksum 
    logger.debug("Payment request Sent (cart cleared) ...... ")

    # Booking Order
    for cartitem in request.cart.cartitem.all():
        orderitem = OrderItem.objects.create(
            order = order,
            item = cartitem.item,
            quantity = cartitem.quantity,
        )

    # empty the cart
    del request.session['cart_id']
    request.cart.delete()
    return render(request , 'pizza/paytm.html', {'paytmParams':paytmParams})

@csrf_exempt
def orderDone(request):
    
    logger.info("POST Payment Request Received...")
    response = request.POST 
    paytmChecksum = ""
    paytmParams = {}
    for key, value in response.items(): 
        if key == 'CHECKSUMHASH':
            paytmChecksum = value
        else:
            paytmParams[key] = value
    
    try:
        order = Order.objects.get(order_id = paytmParams["ORDERID"])
    except Order.DoesNotExist :
        logger.debug("Order Does Not Exist..")
    
    # Verify checksum
    try:
        isValidChecksum = Checksum.verify_checksum(paytmParams, MERCHANT_KEY, paytmChecksum)
    except:
        logger.warning("Wrong Checksum...")
        order.delete()
        return redirect('homepage')
    
    if isValidChecksum:
        logger.debug("Checksum Matched...")
        if paytmParams['RESPCODE'] != '01':
            logger.debug(paytmParams["STATUS"])
            order.delete()
            logger.info("Payment UnSuccessful!!!!")
            return redirect('homepage')
        else:
            logger.debug("Payment Successful...")
            order.transaction_id = paytmParams['TXNID']
            order.status = 2
            order.save()
    else:
        logger.debug(paytmParams["STATUS"])
        order.delete()
        return HttpResponse("CHECK SUM MISMATCHED !!!!")
    
    return render(request,'pizza/tracker.html')

@login_required
def tracker(request):
    return render(request,'pizza/tracker.html')

@login_required
def room(request):
    order = list(Order.objects.filter(user=request.user,status__gt = 1))
    if len(order) :
        order_id = order[-1].order_id
        logger.info(f"Beginning customer service for order {order_id}")
        return render(request,'pizza/chat.html',{'room_name_json':str(order_id)})
    else:
        logger.info("No orders...")
        return redirect('menu')