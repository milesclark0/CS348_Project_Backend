from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.Users.serializers import *
from apps.Users.models import *


# Create your views here.


@api_view(['GET'])
def getCustomers(request):
    customers = Customer.objects.all()
    serializer = CustomerSerializer(customers, many=True)
    return Response(serializer.data)


#gets a customer with id=pk in url (getCustomers/[pk])
@api_view(['GET'])
def getCustomer(request, pk):
    customers = Customer.objects.get(id=pk)
    serializer = CustomerSerializer(customers, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def addCustomer(request):
    serializer = CustomerSerializer(data=request.data)
    if serializer.is_valid():
        #TODO
        #handle logic separate from api in future
        serializer.save()
    return Response(serializer.data)
