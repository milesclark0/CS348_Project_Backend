from email.policy import HTTP
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from apps.Users.serializers import *
from apps.Users.models import *




### Customer Endpoints ###

#Returns list of all customers in db
@api_view(['GET'])
def getCustomers(request):
    try:
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)



#Returns a customer with id=pk in url (getCustomers/[pk])
@api_view(['GET'])
def getCustomer(request, pk):
    try: 
        customers = Customer.objects.get(id=pk)
        serializer = CustomerSerializer(customers, many=False)
        return Response(serializer.data)
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)



@api_view(['POST'])
def addCustomer(request):
    #encrypt password
    request.data['password'] = Customer.encrypt_pass(request.data['password'])
    serializer = CustomerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
