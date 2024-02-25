from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
import uuid


class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    CATEGORY = (
        ('Mystery', 'Mystery'),
        ('Thriller', 'Thriller'),
        ('Sci-Fi', 'Sci-Fi'),
        ('Humor', 'Humor'),
        ('Horror', 'Horror'),
    )

    book_name = models.CharField(max_length=100)
    author = models.CharField(max_length=100, default="")
    category = models.CharField(max_length=100, choices=CATEGORY)
    price = models.FloatField()
    stock = models.IntegerField(default=2)

    def __str__(self):
        return self.book_name


class Shipment(models.Model):
    CATEGORY = (
        ('Regular', 'Regular'),
        ('Fast', 'Fast'),
        ('SuperFast', 'SuperFast'),
        ('Xpress', 'Xpress'),
    )

    shipment_name = models.CharField(max_length=100)
    receiver = models.CharField(max_length=100, default="")
    category = models.CharField(max_length=100, choices=CATEGORY)
    price = models.FloatField()
    stock = models.IntegerField(default=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.shipment_name


def generate_tracking_id():
    # Generate a unique ID using UUID and current date
    uuid_str = uuid.uuid4().hex[:6]  # Extract first 6 characters for conciseness
    date_str = datetime.now().strftime("%Y%m%d")  # YYYYMMDD format
    return f"AWB{date_str}_{uuid_str}"


class Order(models.Model):
    tracking_id = models.CharField(max_length=255, unique=True, blank=True, default=generate_tracking_id)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    items_json = models.CharField(max_length=5000, blank=True)
    price = models.IntegerField(default=0)
    name = models.CharField(max_length=100, blank=True)
    email = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=100, default="")
    phone = models.CharField(max_length=100, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return str(self.user)


class Request_Book(models.Model):
    book_name = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.book_name


class Feedback(models.Model):
    feedback_name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.feedback_name
