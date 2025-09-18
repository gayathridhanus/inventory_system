from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings  

# Custom User model
class User(AbstractUser):
    ROLE_CHOICES = (
        ('Admin', 'Admin'),
        ('Staff', 'Staff'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='Staff')

    def __str__(self):
        return f"{self.username} ({self.role})"


# Product model

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('Electronics', 'Electronics'),
        ('Furniture', 'Furniture'),
        ('Plumbing', 'Plumbing'),
        ('Other', 'Other'),
    ]
    
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Other')
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    supplier = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name



# Sale model
class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)  # ✅

    def __str__(self):
        return f"Sale {self.id} - {self.product.name}- {self.date.strftime('%Y-%m-%d')}"


# Purchase model


class Purchase(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    purchased_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Automatically update product stock
        self.product.quantity += self.quantity
        self.product.save()
        super(Purchase, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"