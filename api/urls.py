from django.urls import path
from api.views import user_views
from api.views import account_views


urlpatterns = [
    path('getCustomers/', user_views.getCustomers),
    path('getCustomers/<str:pk>/', user_views.getCustomer, name="uno"),
    path('addCustomer/', user_views.addCustomer),


    path('login/', account_views.login),
    path('logout/', account_views.logout),
    path('register/', account_views.register),
]
