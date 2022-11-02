from django.db import models

from apps.Users.models import *

# Create your models here.

class Item(models.Model):
    """
        {
            "name": "Hot Fries",
            "price": 5.99,
            "count": 10,
            "rating": 5.0,
            "type": "Snack"
        }
    """
    name = models.CharField(default="", max_length=100, unique=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, null=False)
    count = models.IntegerField(default=0, null=False)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0, null=False)
    type = models.CharField(max_length=100, unique=False)

    def getItem(item_id):
        try:
            item = Item.objects.get(id=item_id)
            json = item.__dict__

            #rename key
            json['item_id'] = json.pop('id', None)
            return json
        except Item.DoesNotExist:
            return None




class CartItem(models.Model):
    """
        {
            "item_id": "1",
            "cart_count": 2
        }
    """
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=False)
    cart_count = models.IntegerField(default=0, null=False)

    def getCartItem(cart_item_id):
        try:
            cart_item = CartItem.objects.get(id=cart_item_id)
            serializer = cart_item.__dict__
            
            #renames and searches for itemwith item_id
            serializer['item'] = Item.getItem(serializer.pop('item_id', None))

            #cleanup unwanted values
            serializer['item'].pop('_state', None)
            serializer.pop('_state', None)
            return serializer
        except CartItem.DoesNotExist:
            return None


class Order(models.Model):
    """
        {
            "total": 11.56,
            "tip": 2.00
        }
    """
    total = models.DecimalField(max_digits=7, decimal_places=2, default=0.0, null=False)
    tip = models.DecimalField(max_digits=7, decimal_places=2, default=0.0, null=False)
    date_time = models.DateTimeField(auto_now_add=True, null=False)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=False)
    items = models.ManyToManyField(CartItem)

    def getOrders(orders):
        new_items = []
        #populate objects in json
        for order in orders:
            for item in order['items'] :
                new_items.append(CartItem.getCartItem(item))
            order['items'] = new_items
            new_items = []
        return orders


class Review(models.Model):
    """
        {
            "rating": 0.0
        }
    """
    rating =models.DecimalField(max_digits=2, decimal_places=1, default=0.0, null=False)
    date_time = models.DateTimeField(auto_now_add=True, null=False)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=False)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, null=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)



