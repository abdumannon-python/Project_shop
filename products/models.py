from django.db import models
from decimal import Decimal

from users.models import User

class Category(models.Model):
    title=models.CharField(max_length=20)
    image=models.ImageField(upload_to='category_image/',null=True,blank=True)

    def __str__(self):
        return self.title

class Products(models.Model):
    auth=models.ForeignKey(User,on_delete=models.CASCADE,related_name='auth')
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='product')
    title=models.CharField(max_length=50)
    brand=models.CharField(max_length=50)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    discount_price=models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    percent=models.IntegerField(null=True,blank=True,default=0)
    main_image=models.ImageField(upload_to='product_image',null=True,blank=True)
    stock=models.PositiveIntegerField()
    desc=models.TextField()

    def save(self,*args,**kwargs):
        price = Decimal(self.price) if self.price not in ['', None] else Decimal('0')
        percent = Decimal(self.percent) if self.percent not in ['', None] else Decimal('0')
        if percent:
            reduction = (price * percent) / 100
            self.discount_price = price - reduction
        else:
            self.discount_price=price
        super().save(*args,**kwargs)
    def __str__(self):
        return self.title
class ProductImages(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='images')
    image=models.ImageField(upload_to='product_images/',null=True,blank=True)


    def __str__(self):
        return self.product.title

class Wishlis(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='wishlis')
    product=models.ForeignKey(Products,on_delete=models.CASCADE,related_name='product')


