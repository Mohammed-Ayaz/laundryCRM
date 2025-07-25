from django.contrib import admin

# Register your models here.

from . models import Record, Customer, Staff, Service, Task, Order, OrderItem

admin.site.register(Record) 
admin.site.register(Customer) 
admin.site.register(Staff) 
admin.site.register(Service) 
admin.site.register(Task) 
admin.site.register(Order)  
admin.site.register(OrderItem) 