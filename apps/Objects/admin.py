from django.contrib import admin
from apps.Objects.models import *
# Register your models here.
admin.site.register(Item)
admin.site.register(Order)
admin.site.register(Review)
admin.site.register(CartItem)

