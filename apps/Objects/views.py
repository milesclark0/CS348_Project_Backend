from django.shortcuts import render
from apps.Objects.models import Item
from django.db import connection

# Create your views here.
def show_items(request):
    cursor = connection.cursor()
    cursor.execute("call GetAllItems()")
    results = cursor.fetchall()
    return render(request, "show_items.html", {'items': results})
    #items = Item.objects.all()
    #return render(request,"show_items.html",{'items':items})