from ast import Or
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from apps.Objects.models import *
from apps.Users.models import Customer
from apps.Objects.serializers import *
from django.db import connection
from django.shortcuts import render


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
    print(items)
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

        #Update Quantities of Each item in Order
        item_changed = Item.objects.get(id=item['item_id'])
        new_quantity = item_changed.count - int(item['cart_count'])
        if new_quantity < 0:
            return Response(data={"message": "Not Enough Stock For This Order!"}, status=status.HTTP_404_NOT_FOUND)
        item_changed.count = item_changed.count - int(item['cart_count'])
        item_changed.save()

    data['items'] = new_items  
    serializer = OrderSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_items(request):
    cursor = connection.cursor()
    cursor.execute("call GetAllItems()")
    results = cursor.fetchall()
    #serializer = ItemSerializer(results, context={'request': request}, many=True)
    #return Response(serializer.data)
    json_data = []
    for row in results:
        json_data.append({"id" : row[0], "name" : row[1], "price": row[2], 
                        "count" : row[3], "rating": row[4], "type": row[5]})
    cursor.close()
    return Response(json_data)
    #return render(request, "show_items.html", {'Item': results})
    """try:
        result = Item.objects.all()
        print(result)
        serializer = ItemSerializer(result, context={'request': request}, many=True)
        return Response(serializer.data)
    except Item.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)  """


@api_view(['POST'])
def get_order_items(request):
    print(request.data)
    cursor = connection.cursor()
    arg = [request.data]
    print(arg)
    cursor.callproc('getOrderItems', arg)
    results = cursor.fetchall()
    data = []
    for row in results:
        data.append({"id": row[0],"item" : row[1], "price" : row[2]})

    cursor.close()
    return Response(data)

@api_view(['POST'])
def add_rating(request):
    employee = None
    item = None 
    customer = None
    order = None
    try:  
        employee = Employee.objects.get(id=request.data.get("employee", None))
    except Employee.DoesNotExist:
        pass
    try:
        item = Item.objects.get(id=request.data.get("item", None))
    except Item.DoesNotExist:
        pass
    try:
        customer = Customer.objects.get(id=request.data.get("customer", None))
    except Customer.DoesNotExist:
        return Response(data={"message": "Could not create review without a specified customer"}, status=status.HTTP_404_NOT_FOUND)
    try:
        order = Order.objects.get(id=request.data.get("order", None))
    except Order.DoesNotExist:
        return Response(data={"message": "Could not create review without a specified order"}, status=status.HTTP_404_NOT_FOUND)
    print(order)
    rating = request.data.get("rating", 0.0)
    try:
        if employee and item:
            return Response(data={"message": "Could not create review with both item and driver specified"}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer=ReviewSerializer(data=request.data, many=False)
            if serializer.is_valid():
                if item:
                    Review.objects.update_or_create(customer=customer, item=item, defaults={'rating': rating, 'order': order})
                else:
                    Review.objects.update_or_create(customer=customer, employee=employee, order=order, defaults={'rating': rating})
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(data={"message": str(e)}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_open_jobs(request,):
    cursor = connection.cursor()
    cursor.execute("call getOpenJobs()")
    fields = [desc[0] for desc in cursor.description]
    jobs = cursor.fetchall()
    cursor.close()

    return Response([dict(zip(fields, job)) for job in jobs])

@api_view(['POST'])
def accept_job(request):
    data = request.data
    try:
        order = Order.objects.get(id=data["orderID"])
        order.employee_id = data["empID"]
        order.save()
    except Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    return Response("HELLO!")
