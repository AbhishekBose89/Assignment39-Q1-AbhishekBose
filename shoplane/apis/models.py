from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Create your models here.
# class User(models.Model):
#     first_name = models.CharField(max_length=200)
#     last_name = models.CharField(max_length=200)
#     username = models.CharField(max_length=300, unique=True)
#     email = models.EmailField(max_length=300, unique=True)
#     mobile_number = models.IntegerField()
#     password = models.CharField(max_length=20)


class UserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError("Username should be provided")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, password, **extra_fields)


class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    password = models.CharField(max_length=20)
    username = models.CharField(max_length=200, unique=True)

    USERNAME_FIELD = "username"
    objects = UserManager()


class Order(models.Model):
    user = models.IntegerField()
    order_number = models.IntegerField()
    order_date = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    order = models.IntegerField()
    product = models.IntegerField()
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Review(models.Model):
    product = models.IntegerField()
    user = models.IntegerField()
    rate = models.DecimalField(max_digits=2, decimal_places=1)
    review = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)


class Product(models.Model):
    name = models.CharField(max_length=200)
    image = models.TextField()
    brand = models.CharField(max_length=200)
    shipping = models.TextField(default=True, null=True)
    description = models.TextField()
    price = models.IntegerField()
    category = models.CharField(max_length=200)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["name"], name="name-index"),
            models.Index(fields=["category", "brand"], name="category-brand-index"),
        ]


class BillingAddress(models.Model):
    order = models.IntegerField(unique=True)
    address = models.TextField()
    city = models.CharField(max_length=200)


class Coupon(models.Model):
    orders = models.ManyToManyField(Order, related_name="coupons")
    code = models.CharField(max_length=200)
    discount = models.DecimalField(decimal_places=1, max_digits=2)
