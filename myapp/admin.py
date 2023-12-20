from django.contrib import admin

# Register your models here.

from myapp.models import Vendor
from myapp.models import PurchaseOrder



# admin.py
from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.db import models

# Import your custom user model
from myapp.models import CustomUser

class MyAdminLogEntry(LogEntry):
    custom_user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        # Add the following line to make sure it doesn't create a database table for MyAdminLogEntry
        abstract = True

# Create a concrete model
class ConcreteAdminLogEntry(MyAdminLogEntry):
    class Meta:
        # Remove the abstract attribute
        abstract = False

# Register the concrete model with the admin
admin.site.register(ConcreteAdminLogEntry)




    

class con(admin.ModelAdmin):

    list_display = ('name','contact_details','address','vendor_code','on_time_delivery_rate','quality_rating_avg','average_response_time','fulfillment_rate') 
    
class con2(admin.ModelAdmin):

    list_display = ('vendor','po_number','order_date','delivery_date','items','quantity','status','quality_rating','issue_date','acknowledgment_date')       
    

admin.site.register(Vendor, con)
admin.site.register(PurchaseOrder, con2)