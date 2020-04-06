import logging
import aioredis
from channels.generic.websocket import AsyncJsonWebsocketConsumer,WebsocketConsumer
from channels.consumer import SyncConsumer , AsyncConsumer
from channels.db import database_sync_to_async
from .models import *
from pprint import pprint

logger = logging.getLogger(__name__)

class ChatConsumer(AsyncJsonWebsocketConsumer):
    
    EMPLOYEE = 2
    CLIENT = 1

    @database_sync_to_async
    def get_user_type(self,user,order_id):

        try:
            order = Order.objects.get(order_id = order_id)
        except : 
            logger.error('Order not found..')
        if(user == order.user):
            return self.CLIENT
        elif user.is_employee :
            order.last_spoken_to = user
            order.save()
            return self.EMPLOYEE
        else:
            return None

    async def connect(self):
        logger.debug("Connecting..")
        self.order_id = self.scope['url_route']['kwargs']['order_id']
        self.room_group_name = f"customer_service_{self.order_id}"
        
        if self.scope['user'].is_anonymous:
            logger.debug('No User Present!! Closing Websocket ....')
            await self.close()
        
        user = await self.get_user_type(self.scope['user'],self.order_id)
        
        authorized = False        
        if user == self.EMPLOYEE :
            logger.info(f"Openning chat stream for employee {self.scope['user'].get_full_name()}")
            authorized = True

        elif user == self.CLIENT:
            logger.info(f"Openning chat stream for User {self.scope['user'].get_full_name()}")
            authorized = True 

        else:
            logger.info(f"Unauthorised access from User {self.scope['user'].get_full_name()}")
            authorized = False

        if not authorized:
            logger.debug("Closing , because not authorised")
            await self.close()

        else:
            logger.debug("Authorised...")
            self.r_conn = await aioredis.create_redis('redis://localhost')
            await self.channel_layer.group_add(self.room_group_name,self.channel_name)
            await self.accept()
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type':'join',
                    'username':self.scope['user'].get_full_name(),
                }
            )
    
    async def disconnect(self, close_code):
        logger.debug("DisConnecting..")
        if not self.scope['user'].is_anonymous :
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type':'leave',
                    'username':self.scope['user'].get_full_name(),
                }
            )
            logger.info(f"Disconnecting {self.scope['user'].get_full_name()} Session")
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name,
            )

    async def receive_json(self, content):
        typ = content.get('type')
        if typ == 'message':
            logger.info("Received Message")
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type':'message',
                    'username':self.scope['user'].get_full_name(),
                    'message':content['message'],
                },
            )

        elif typ == 'heartbeat':
            logger.info("heartbeat..")
            await self.r_conn.setex(
                f"{self.room_group_name}_{self.scope['user'].email}",10,"1",
            )   
        else:
            logger.debug("Neither heartbeat nor Message Received..")
    
    async def join(self,event):
        logger.debug(event)
        await self.send_json(event)

    async def leave(self,event):
        logger.debug(event)
        await self.send_json(event)

    async def message(self,event):
        logger.debug(event)
        await self.send_json(event)
        