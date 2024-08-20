from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
import razorpay

# Create your models here.
class Category(models.Model):
    category_name=models.CharField(max_length=100)
    category_img=models.ImageField(upload_to='products',default='')
    class Meta:
        db_table='categories'
    def __str__(self):
        return self.category_name

class Unit(models.Model):
    unit_name=models.CharField(max_length=20)
    class Meta:
        db_table='units'
    def __str__(self):
        return self.unit_name
    
class Currency(models.Model):
    currency_symbol=models.CharField(max_length=10)
    class Meta:
        db_table='currency'
    def __str__(self):
        return self.currency_symbol

class Product(models.Model):
    category=models.ForeignKey(Category, blank=False , null=False , on_delete=models.CASCADE) #if we delete the category then it will also delete that related product 
    product_name=models.CharField(max_length=100)
    product_img=models.ImageField(upload_to='products',default='')
    product_quantity=models.IntegerField()
    product_unit=models.ForeignKey(Unit, blank=False , null=False , on_delete=models.PROTECT) #this will not delete product but will delete unit
    product_currency=models.ForeignKey(Currency, blank=False , null=False , on_delete=models.PROTECT)
    product_price=models.CharField(max_length=20)
    class Meta:
        db_table='products'
    def __str__(self):
        return self.product_name
    
class Cart(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    subtotalprice=models.FloatField(default=0.00)
    class Meta:
        db_table='cart'
        unique_together = ('product', 'user')

    def save(self, *args, **kwargs):
        self.subtotalprice = int(self.product.product_price) * int(self.quantity)
        super().save(*args, **kwargs)

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.user.username} - {self.address_line_1}, {self.city}, {self.state}, {self.zip_code}'