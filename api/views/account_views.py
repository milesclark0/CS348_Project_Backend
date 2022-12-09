from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from apps.Users.models import *
from apps.Users.serializers import *
from django.contrib.auth import authenticate




### Account Endpoints ###

#Logs user in and returns user
@api_view(['POST'])
def login(request):
    data = {}
    user = Customer.login(request)
    if user:
        serializer = CustomerSerializer(user, many=False)
        return Response(serializer.data)

    user = Manager.login(request)
    if user:
        serializer = ManagerSerializer(user, many=False)
        return Response(serializer.data)
    
    user = Employee.login(request)
    if user:
        serializer = ManagerSerializer(user, many=False)
        return Response(serializer.data)

    data['message'] = "Incorrect Username or Password"
    return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def changePassword(request):
    data = {}
    username = request.data['username']
    user = None
    code = None

    if request.data['password'] != request.data['password2']:
        data['message'] = "Passwords Do Not Match!"
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    try:
        user = Customer.objects.get(username=username)
        code = 1
    except Customer.DoesNotExist:
        try:
            user = Manager.objects.get(username=username)
            code = 2
        except Manager.DoesNotExist:
            try:
                user = Employee.objects.get(username=username)
                code = 3
            except Employee.DoesNotExist:
                pass

    if user and code == 1:
        user = Customer.changePassword(request)
        if user:
            serializer = CustomerSerializer(user, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
    elif user and code == 2:
        user = Manager.changePassword(request)
        if user:
            serializer = ManagerSerializer(user, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
    elif user and code == 3:
        user = Employee.changePassword(request)
        if user:
            serializer = EmployeeSerializer(user, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        data['message'] = "Password Change Failed"
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    


@api_view(['POST'])
def register(request):
    #encrypt password
    request.data['password'] = Customer.encrypt_pass(request.data['password'])
    serializer = CustomerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def hire(request):
    request.data['password'] = Employee.encrypt_pass(request.data['password'])
    serializer = EmployeeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def fire(request, employee_id):
    user = None
    try: 
        user = Employee.objects.get(id=employee_id)
        user.delete()
    except Employee.DoesNotExist as e:
        return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_200_OK)

