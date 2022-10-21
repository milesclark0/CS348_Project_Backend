# Create your models here.
from django.db import models
import hashlib


# Create your models here.
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
