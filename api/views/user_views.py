from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from apps.Users.serializers import *
from apps.Users.models import *
from django.db import connection




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


@api_view(['GET'])
def getEmployees(request, manager_id):

    cursor = connection.cursor()
    cursor.execute("call getEmployees({manager_id})".format(manager_id=manager_id))
    fields = [desc[0] for desc in cursor.description]
    employees = cursor.fetchall()

    return Response([dict(zip(fields, employee)) for employee in employees])

@api_view(['GET'])
def getJobs(request, employee_id):
    cursor = connection.cursor()
    cursor.execute("call getJobs({employee_id})".format(employee_id=employee_id))
    fields = [desc[0] for desc in cursor.description]
    jobs = cursor.fetchall()
    cursor.close()

    return Response([dict(zip(fields, job)) for job in jobs])

