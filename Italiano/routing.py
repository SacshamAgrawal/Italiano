from channels.routing import ProtocolTypeRouter , URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from pizza.consumers import *

application = ProtocolTypeRouter({
    'websocket':AuthMiddlewareStack(
        URLRouter([
            path('ws/<slug:order_id>/',ChatConsumer ) ,
        ]),
    ),
})