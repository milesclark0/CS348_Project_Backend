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
    
@api_view(['POST'])
def create_order(request):
    #Check if cart items exist
    data = request.data
    items = data['items']
    new_items = []
    for item in items:
        item_exists = CartItem.objects.filter(item_id=item['item_id'], cart_count=item['cart_count']).exists()
        cart_item = item["item_id"]
        if not item_exists:
            #create cart item if it doesn't exist
            try:
                CartItem.objects.create(item_id=item['item_id'], cart_count=item['cart_count'])
            except CartItem.DoesNotExist:
                return Response(data={"message": "Could not create or find cart item"}, status=status.HTTP_404_NOT_FOUND)
        new_items.append(cart_item)
    data['items'] = new_items  
    serializer = OrderSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_items(request):
    try:
        result = Item.objects.all()
        serializer = ItemSerializer(result, context={'request': request}, many=True)
        return Response(serializer.data)
    except Item.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)   
