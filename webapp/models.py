from django.db import models
from django.contrib.auth.models import User



class Record(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=255)
    province = models.CharField(max_length=200)
    country = models.CharField(max_length=125)

    def __str__(self):
        return self.first_name + "   " + self.last_name


class Customer(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=255)
    province = models.CharField(max_length=200)
    country = models.CharField(max_length=125)
    special_instructions = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Staff(models.Model):
    POSITION_CHOICES = [
        ('ADMIN', 'Administrator'),
        ('MANAGER', 'Manager'),
        ('STAFF', 'Staff Member'),
        ('DRIVER', 'Delivery Driver'),
        ('WASHER', 'Washer'),
        ('PRESSER', 'Presser'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=20, choices=POSITION_CHOICES)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=300, blank=True, null=True)
    hire_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.get_position_display()})"


class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    estimated_duration = models.DurationField() 
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} - ${self.price}"



class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('RECEIVED', 'Received'),
        ('WASHING', 'Washing'),
        ('PRESSING', 'Pressing'),
        ('READY', 'Ready for Delivery'),
        ('DELIVERING', 'Out for Delivery'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    pickup_date = models.DateTimeField(blank=True, null=True)
    delivery_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    assigned_staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)
    special_instructions = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Order #{self.id} - {self.customer} ({self.get_status_display()})"
    
    def calculate_total(self):
        return sum(item.subtotal() for item in self.order_items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    
    def save(self, *args, **kwargs):
        if not self.unit_price and self.service_id:
            self.unit_price = self.service.price
        super().save(*args, **kwargs)
    
    def subtotal(self):
        return self.unit_price * self.quantity
    
    def __str__(self):
        return f"{self.quantity} x {self.service.name} @ {self.unit_price}"
    

class Payment(models.Model):
    PAYMENT_METHODS = [
        ('CASH', 'Cash'),
        ('CARD', 'Credit/Debit Card'),
        ('TRANSFER', 'Bank Transfer'),
        ('MOBILE', 'Mobile Payment'),
    ]
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    transaction_reference = models.CharField(max_length=100, blank=True, null=True)
    is_completed = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Payment of {self.amount} for Order #{self.order.id}"


class Inventory(models.Model):
    item_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    unit = models.CharField(max_length=20)
    reorder_level = models.PositiveIntegerField()
    last_restocked = models.DateField(auto_now=True)
    
    def __str__(self):
        return f"{self.item_name} ({self.quantity} {self.unit})"
    
    def needs_restock(self):
        return self.quantity <= self.reorder_level


class Task(models.Model):
    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    ]
    
    assigned_to = models.ForeignKey(Staff, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateTimeField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='MEDIUM')
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.title} - {self.assigned_to}"
