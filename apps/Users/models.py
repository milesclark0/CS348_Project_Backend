from django.db import models

# Create your models here.
from django.db import models


# Create your models here.
class Customer(models.Model):
    username = models.CharField(max_length=50, unique=True, null=False)
    password = models.CharField(max_length=50, unique=False, null=False)
    name = models.CharField(max_length=50, unique=False, null=False)
    address = models.CharField(max_length=100, unique=False)
    phone = models.CharField(unique=True, max_length=11)
    birth_date = models.DateField()
    points = models.IntegerField(default=0, null=False)
    creation_date = models.DateField(auto_now_add=True, null=False)

