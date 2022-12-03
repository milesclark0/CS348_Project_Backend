from django.shortcuts import render
from apps.Objects.models import Item

# Create your views here.
def show_items(request):
    items = Item.objects.all()
    return render(request,"show_items.html",{'items':items})