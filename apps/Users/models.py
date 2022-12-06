# Create your models here.
from django.db import models
import hashlib


# Create your models here.
class Manager(models.Model):
    """
        {
            "username": "username",
            "password": "password",
            "name": "name",
            "zip": "address",
            "phone": "1234567890",
            "birth_date": "2000-01-01",
        }
    """
    username = models.CharField(max_length=50, unique=True, null=False)
    password = models.CharField(max_length=50, unique=False, null=False)
    name = models.CharField(max_length=50, unique=False, null=False)
    zip = models.CharField(max_length=100, unique=False)
    phone = models.CharField(unique=True, max_length=11)
    birth_date = models.DateField()
    hire_date = models.DateField(auto_now_add=True, null=False)



    def encrypt_pass(password: str):
        salt = "4Yv"
        # Adding salt at the last of the password
        dataBase_password = password+salt
        # Encoding the password
        hashed = hashlib.md5(dataBase_password.encode())
        return hashed.hexdigest()

class Customer(models.Model):
    """
        {
            "username": "username",
            "password": "password",
            "name": "name",
            "address": "address",
            "phone": "1234567890",
            "birth_date": "2000-01-01",
            "points": 0
        }
    """
    username = models.CharField(max_length=50, unique=True, null=False)
    password = models.CharField(max_length=50, unique=False, null=False)
    name = models.CharField(max_length=50, unique=False, null=False)
    address = models.CharField(max_length=100, unique=False)
    phone = models.CharField(unique=True, max_length=11)
    birth_date = models.DateField()
    points = models.IntegerField(default=0, null=False)
    creation_date = models.DateField(auto_now_add=True, null=False)


    def encrypt_pass(password: str):
        salt = "5gz"
        # Adding salt at the last of the password
        dataBase_password = password+salt
        # Encoding the password
        hashed = hashlib.md5(dataBase_password.encode())
        return hashed.hexdigest()

    def login(request):
        username = request.data['username']
        password = request.data['password']
        user = None
        try:
            user = Customer.objects.get(username=username)
        except Customer.DoesNotExist:
            pass
        if user:
            auth = user.password == Customer.encrypt_pass(password)
            if auth:
                return user
        return None
    
    def changePassword(request):
        username1 = request.data['username']
        password = request.data['password']
        user = None
        try: 
            user = Customer.objects.filter(username=username1)
            user.update(password=Customer.encrypt_pass(password))
        except Customer.DoesNotExist:
            pass
        if user:
            return user[0]
        return None

class Employee(models.Model):
    """
        {
            "username": "username",
            "password": "password",
            "name": "name",
            "zip": "address",
            "phone": "1234567890",
            "birth_date": "2000-01-01",
            "avg_rating": 0.0
        }
    """
    username = models.CharField(max_length=50, unique=True, null=False)
    password = models.CharField(max_length=50, unique=False, null=False)
    name = models.CharField(max_length=50, unique=False, null=False)
    zip = models.CharField(max_length=100, unique=False)
    phone = models.CharField(unique=True, max_length=11)
    birth_date = models.DateField()
    avg_rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0, null=False)
    hire_date = models.DateField(auto_now_add=True, null=False)
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE, null=False)


    def encrypt_pass(password: str):
        salt = "7Jd"
        # Adding salt at the last of the password
        dataBase_password = password+salt
        # Encoding the password
        hashed = hashlib.md5(dataBase_password.encode())
        return hashed.hexdigest()




