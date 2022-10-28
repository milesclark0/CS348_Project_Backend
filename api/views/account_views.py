from email.policy import HTTP
import re
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from apps.Users.models import *
from apps.Users.serializers import *




### Account Endpoints ###

#Logs user in and returns user
@api_view(['POST'])
def login(request):
    username = request.data['username']
    password = request.data['password']
    data = {}
    user = None
    try:
        user = Customer.objects.get(username=username);
    except Customer.DoesNotExist:
        pass
    if user:
        auth = user.password == Customer.encrypt_pass(password)
        if auth:
            serializer = CustomerSerializer(user, many=False)
            #request.session['user'] = serializer.data
            return Response(serializer.data)
    data['message'] = "Incorrect Username or Password"
    return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)


#Logs user out
#Probably wont be used
@api_view(['POST'])
def logout(request):
    data = {}
    try: 
        if request.session['user']:
            print(request.session['user'])
            if request.data["username"] == request.session['user']['username']:
                del request.session['user']
                data["message"] = "User Logged Out"
                return Response(data=data, status=status.HTTP_202_ACCEPTED)
    except KeyError:
        pass
    data["message"] = "Could not log out specified user"
    return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def register(request):
    #encrypt password
    request.data['password'] = Customer.encrypt_pass(request.data['password'])
    serializer = CustomerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

