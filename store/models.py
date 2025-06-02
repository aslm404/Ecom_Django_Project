from django.db import models
from django.contrib.auth.models import User
import uuid
import os


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4().hex}.{ext}"
    return os.path.join('uploads/', filename)


class Category(models.Model):
    slug = models.CharField(max_length=150)
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to=get_file_path)
    description = models.TextField(max_length=500)
    status = models.BooleanField(default=False, help_text='0=Visible, 1=Hidden')
    trending = models.BooleanField(default=False, help_text='0=Not Trending, 1=Trending')
    meta_title = models.CharField(max_length=100)
    meta_keyword = models.CharField(max_length=100)
    meta_description = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.SlugField()
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to=get_file_path)
    small_description = models.TextField(max_length=150)
    quantity = models.IntegerField()
    description = models.TextField(max_length=500)
    original_price = models.FloatField()
    selling_price = models.FloatField()
    status = models.BooleanField(default=False, help_text='0=Visible, 1=Hidden')
    trending = models.BooleanField(default=False, help_text='0=Not Trending, 1=Trending')
    tag = models.CharField(max_length=150)
    meta_title = models.CharField(max_length=100)
    meta_keyword = models.CharField(max_length=100)
    meta_description = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_qty = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


ORDER_STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('Out for shipping', 'Out for shipping'),
    ('Completed', 'Completed')
]

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    email = models.CharField(max_length=150)
    phone = models.CharField(max_length=100)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    pincode = models.CharField(max_length=50)
    total_price = models.FloatField()
    payment_mode = models.CharField(max_length=150)
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=150, choices=ORDER_STATUS_CHOICES, default='Pending')
    message = models.TextField(blank=True, default='')
    tracking_no = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} - {self.tracking_no}"


class Orderitem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.order.tracking_no} - {self.product.name}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    pincode = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
