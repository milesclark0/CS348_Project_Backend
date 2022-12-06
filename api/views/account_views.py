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
    data['message'] = "Incorrect Username or Password"
    return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def changePassword(request):
    data = {}
    if request.data['password'] != request.data['password2']:
        data['message'] = "Passwords Do Not Match!"
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    user = Customer.changePassword(request)
    if user:
        serializer = CustomerSerializer(user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
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

