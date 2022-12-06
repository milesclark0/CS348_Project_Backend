from django.urls import path
from api.views import user_views
from api.views import account_views
from api.views import object_views


urlpatterns = [
    path('getCustomers/', user_views.getCustomers),
    path('getCustomers/<str:pk>/', user_views.getCustomer, name="uno"),
    path('addCustomer/', user_views.addCustomer),


    path('login/', account_views.login),
    path('register/', account_views.register),
    path('changePassword/', account_views.changePassword),
    path('hire/', account_views.hire),

    path('getRecentOrder/<str:customer_id>', object_views.get_recent_order),
    path('getOrders/<str:customer_id>', object_views.get_orders),
    path('createOrder/', object_views.create_order),
    

    path('getItems/', object_views.get_items),
]
