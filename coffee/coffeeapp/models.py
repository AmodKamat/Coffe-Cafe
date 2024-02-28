from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    CATEGORY_CHOICES=[
        (1,"COFFEE"),
        (2,"DRINKS"),
        (3,"DESSERTS"),
        (4,"BURGUR")
    ]
    name=models.CharField(max_length=100,verbose_name="Product Name")
    price=models.FloatField(verbose_name="Product Price")
    pdetails=models.CharField(max_length=200, verbose_name="Product Details")
    category=models.IntegerField(choices=CATEGORY_CHOICES)
    is_active=models.BooleanField(default=True,verbose_name="Available")
    pimage=models.ImageField(upload_to="images")
    

    def __str__(self):
        return self.name
    
class Cart(models.Model):
    uid=models.ForeignKey(User,on_delete=models.CASCADE)
    pid=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)

class Order(models.Model):
    order_id=models.CharField(max_length=100)
    uid=models.ForeignKey(User,on_delete=models.CASCADE)
    pid=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)




    

