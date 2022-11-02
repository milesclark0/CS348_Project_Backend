from ast import Or
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from apps.Objects.models import *
from apps.Users.models import Customer
from apps.Objects.serializers import *



### Object Endpoints ###

#gets a users orders, returns most recent
@api_view(['GET'])
def get_recent_order(request, customer_id):
    try:
        recent_order = Order.objects.filter(customer_id=customer_id).order_by('-date_time')[0:1].get()
        serializer = OrderSerializer(recent_order, many=False)
        new_items = []
        orders = [serializer.data]
        result = Order.getOrders(orders)
        
        return Response(result[0])
    except Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_orders(request, customer_id):
    try:
        recent_order = Order.objects.filter(customer_id=customer_id).order_by('-date_time')
        serializer = OrderSerializer(recent_order, many=True)
        orders = serializer.data
        result = Order.getOrders(orders)
        
        return Response(result)
    except Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)   

