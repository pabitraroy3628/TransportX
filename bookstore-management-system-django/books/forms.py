from django import forms
from .models import Book, Request_Book, Shipment
from django.contrib.auth.models import User


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class ShipmentForm(forms.ModelForm):
    class Meta:
        model = Shipment
        # fields = '__all__'
        fields = ('shipment_name', 'receiver', 'category', 'price', 'stock')

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # Create a hidden field for user and set its value to current user
    #     self.fields['user_id'] = forms.HiddenInput(initial=self.request.user)


class RequestBookForm(forms.ModelForm):
    class Meta:
        model = Request_Book
        fields = ('book_name', 'author')
