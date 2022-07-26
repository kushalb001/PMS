from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.db.models.fields import CommaSeparatedIntegerField
from django_countries.fields import CountryField
# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Medicine(models.Model):
    name=models.CharField(max_length=255)
    category=models.ForeignKey(Category,on_delete=models.SET_NULL, null=True)
    description = models.TextField(null=True, blank=True)
    image = models.FileField(blank=True)
    
    quantity=models.IntegerField(default=0)
    ali = models.BooleanField(default=False)
    price = models.FloatField()
    def __str__(self):
        return self.name





    
    
   
class Address(models.Model):
    street_address = models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100) 


class Customer(models.Model):
    first_name=models.CharField(max_length=255)
    middle_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    phno=models.CharField(max_length=10,unique=True)
    
    DOB=models.DateField(auto_now=False, auto_now_add=False)
    address=models.ForeignKey(Address,on_delete=models.SET_NULL,null=True)
    def __str__(self):
        return self.first_name


        
class OrderItem(models.Model):
    
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.name}"

    def get_final_price(self):
        return self.quantity * self.item.price


    
    


class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)                         
    
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date=models.DateTimeField()
    ordered = models.BooleanField(default=False)
    
    

    def __str__(self):
        return self.customer.first_name

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        
        return total




class Prescription(models.Model):
    image = models.ImageField(null=True)
    order=models.ForeignKey(Order,on_delete=CASCADE)
    def __str__(self):
        return str(self.id)

class Covid(models.Model):
    customer=models.OneToOneField(Customer, on_delete=models.CASCADE)
    no_of_days=models.IntegerField(null=True)
    cold=models.BooleanField(default=False,null=True,blank=True)
    fever=models.BooleanField(default=False,null=True,blank=True)
    breathing_difficulty=models.BooleanField(default=False,null=True,blank=True)
    comorbid=models.BooleanField(default=False,null=True,blank=True)
    start_date = models.DateField(auto_now_add=True)





