from django.urls import path
from api import views

urlpatterns = [
    path('getCustomers/', views.getCustomers),
    path('getCustomers/<str:pk>/', views.getCustomer, name="uno"),
    path('addCustomer/', views.addCustomer)
]
