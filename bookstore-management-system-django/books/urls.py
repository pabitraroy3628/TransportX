from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.Usersignup, name="Usersignup"),
    path("user_login/", views.User_login, name="User_login"),
    path("logout/", views.Logout, name="Logout"),
    
#     For admin
#     path("all_books/", views.Admin, name="Admin"),
    path("all_shipments/", views.Admin, name="Admin"),
    path("customers_list/", views.customers_list, name="customers_list"),
    # path("add_books/", views.Add_Books, name="add_new_books"),
    path("add_shipments/", views.Add_Shipments, name="add_new_shipments"),
    path("track_orders/", views.track_orders, name="track_orders"),
    path("update_details/", views.update_details, name="update_user_detils"),
    path("update_status/", views.update_status, name="update_delivery_status"),
    # path("all_books/delete_<int:myid>/", views.Delete_Books, name="delete_book"),
    path("all_shipments/delete_<int:myid>/", views.Delete_Shipments, name="delete_shipment"),
    # path("see_requested_books/", views.see_requested_books, name="see_requested_books"),
    path("see_feedbacks/", views.see_feedbacks, name="see_feedbacks"),
    # path("delete_requested_books/delete_<int:myid>/", views.delete_requested_books, name="delete_requested_books"),
    path("delete_feedbacks/delete_<int:myid>/", views.delete_feedbacks, name="delete_feedbacks"),
    path("customers_list/orders_<int:myid>/", views.orders_list, name="orders_list"),
    path("customers_list/orders_<int:myid>/data/", views.data_view, name="data"),
 
    
#     For customers
    path("for_users/", views.Users, name="Users"),
    path("request_feedback/", views.request_feedback, name="request_feedback"),
    path("checkout/", views.checkout, name="checkout"),    
]
