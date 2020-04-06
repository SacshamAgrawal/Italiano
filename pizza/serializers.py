from rest_framework import serializers, reverse
from .models import *

class OrderSerializer(serializers.ModelSerializer):

    order_items = serializers.SerializerMethodField()
    
    class Meta:
        model = Order 
        fields = ('url','user','order_id','billing_address','status','transaction_id','amount','order_items','time_of_order')
        read_only_fields = ('url','user','order_id','transaction_id','amount','time_of_order')

    def get_order_items(self,obj):
        order_items = []
        for orderitem in obj.orderitem.all():
            order_items.append(
                {
                    'item':orderitem.item.name,
                    'quantity':orderitem.quantity,
                },
            )
        return order_items

    