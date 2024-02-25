from datetime import datetime
from uuid import uuid4

from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .decorators import restricted_login, admin_or_user
from .forms import BookForm, RequestBookForm, ShipmentForm, UserUpdateForm
from .models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


def index(request):
    return render(request, "index.html")


def Usersignup(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == "POST":
            username = request.POST['username']
            email = request.POST['email']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            if len(username) > 15:
                messages.info(request, "Username must be under 15 characters.")
                return redirect('/signup')
            if not username.isalnum():
                messages.info(request, "Username must contain only letters and numbers.")
                return redirect('/signup')
            if password1 != password2:
                messages.info(request, "Passwords do not match.")
                return redirect('/signup')

            user = User.objects.create_user(username, email, password1)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            return render(request, 'user_login.html')
    return render(request, "signup.html")


def User_login(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == "POST":
            user_username = request.POST['user_username']
            user_password = request.POST['user_password']

            user = authenticate(username=user_username, password=user_password)

            if user is not None:
                login(request, user)
                messages.success(request, "Successfully Logged In")
                return redirect("/for_users")
            else:
                messages.error(request, "Please provide a valid username and password")
    return render(request, "user_login.html")


def Logout(request):
    # logout(request)
    thank = True
    # return render(request, "index.html", {'thank': thank})
    return redirect('/request_feedback')
    # return render(request, "index.html", {'thank': thank})


@admin_or_user
def Admin(request):
    # books = Book.objects.all()
    # total_books = books.count()
    print('hi')
    print(request.user)
    shipments = Shipment.objects.all()
    total_shipments = shipments.count()
    return render(request, "for_admin.html", {'shipments': shipments, 'total_shipments': total_shipments})


def Delete_Books(request, myid):
    books = Book.objects.get(id=myid)
    if request.method == "POST":
        books.delete()
        return redirect('/all_books')
    return render(request, 'delete_book.html', {'books': books})


def Delete_Shipments(request, myid):
    shipments = Shipment.objects.get(id=myid)
    if request.method == "POST":
        shipments.delete()
        return redirect('/all_shipments')
    return render(request, 'delete_shipment.html', {'shipments': shipments})


@login_required(login_url='/user_login')
def Users(request):
    # books = Book.objects.all()
    # total_books = books.count()
    current_user = request.user
    shipments = Shipment.objects.filter(user=current_user)
    total_shipments = shipments.count()
    return render(request, "for_user.html", {'shipments': shipments, 'total_shipments': total_shipments})


def Add_Shipments(request):
    if request.method == "POST":
        # form = BookForm(request.POST)
        form = ShipmentForm(request.POST)
        if form.is_valid():
            current_user = request.user
            # Assign the user to the form instance
            form.instance.user = current_user
            form.save()
            return render(request, "add_shipments.html", {'submitted': True})
    else:
        form = ShipmentForm()
    return render(request, "add_shipments.html", {'form': form})


def track_orders(request):
    current_user = request.user
    orders = Order.objects.filter(user=current_user)
    total_orders = orders.count()
    print(orders)
    return render(request, "track_orders.html", {'orders': orders, 'total_orders': total_orders})


def update_details(request):
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/for_users')  # Redirect to profile page after update
        else:
            # Handle form errors (optional)
            return render(request, 'edit_user_details.html', {'form': form})
    else:
        form = UserUpdateForm(request.POST, instance=request.user)
        return render(request, 'edit_user_details.html', {'form': form})

def update_status(request):
    if request.method == "POST":
        tracking_id = request.POST.get('tracking_id')
        new_status = request.POST.get('status')
        customer_id = request.POST.get('customer_id')
        order = Order.objects.get(tracking_id=tracking_id)
        order.status = new_status
        order.save()

        return redirect(f'/customers_list/orders_{customer_id}/')
def request_feedback(request):
    if request.method == "POST":
        user = request.user
        print(user)
        # book_name = request.POST['book_name']
        # author = request.POST['author']
        print(request)
        feedback_name = request.POST['feedback_name']
        description = request.POST['description']
        # book = Request_Book(user=user, book_name=book_name, author=author)
        # book.save()
        feedback = Feedback(user=user, feedback_name=feedback_name, description=description)
        feedback.save()
        thank = True
        logout(request)
        # return render(request, "request_books.html", {'thank': thank})
        return render(request, "index.html", {'thank': thank})
    return render(request, "request_books.html")


def see_requested_books(request):
    requested_book = Request_Book.objects.all()
    requested_books_count = requested_book.count()
    return render(request, "see_requested_books.html",
                  {'requested_book': requested_book, 'requested_books_count': requested_books_count})


def see_feedbacks(request):
    feedback = Feedback.objects.all()
    feedback_count = feedback.count()
    return render(request, "see_feedbacks.html",
                  {'feedback': feedback, 'feedback_count': feedback_count})


def delete_requested_books(request, myid):
    delete_book = Request_Book.objects.get(id=myid)
    if request.method == "POST":
        delete_book.delete()
        return redirect('/see_requested_books')
    return render(request, "delete_requested_books.html", {'delete_book': delete_book})


def delete_feedbacks(request, myid):
    delete_feedback = Feedback.objects.get(id=myid)
    if request.method == "POST":
        delete_feedback.delete()
        return redirect('/see_feedbacks')
    return render(request, "delete_feedback.html", {'delete_feedback': delete_feedback})


def customers_list(request):
    customers = Order.objects.all()
    customer_count = customers.count()
    return render(request, "customers_list.html", {'customers': customers, 'customer_count': customer_count})


def orders_list(request, myid):
    customer = Order.objects.filter(id=myid)
    customers = Order.objects.all()
    print('---------')
    print(repr(customer))
    return render(request, "orders_list.html", {'customer': customer, 'customers': customers})


def data_view(request, myid):
    orders = Order.objects.get(id=myid)
    return JsonResponse({'data': orders.items_json})


def checkout(request):
    if request.method == "POST":
        user = request.user
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        price = request.POST.get('price', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address', '')
        phone = request.POST.get('phone', '')
        status = 'Ordered'

        order = Order(user=user, items_json=items_json, name=name, email=email, address=address, phone=phone,
                      price=price, status=status)
        order.save()
        thank = True
        return render(request, 'mycart.html', {'thank': thank})
    return render(request, "mycart.html")
