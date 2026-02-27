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


class Wishlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='wishlist')
    product=models.ForeignKey(Products,on_delete=models.CASCADE,related_name='product')

class Chat(models.Model):
    participants=models.ManyToManyField(User,related_name='chats')
    created_at = models.DateTimeField(auto_now_add=True)

    def get_recipient(self, current_user):
        return self.participants.exclude(id=current_user.id).first()
    def last_message(self):
        return self.messages.all().last()



class Messages(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='sent_message')
    product=models.ForeignKey(Products,on_delete=models.CASCADE,null=True,blank=True,related_name='shared_posts')
    chat=models.ForeignKey(Chat,on_delete=models.CASCADE,related_name='messages')
    created_at=models.DateTimeField(auto_now_add=True)
    image=models.ImageField(upload_to='message_images',null=True,blank=True)
    text = models.TextField(null=True,blank=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering=['created_at']

    def __str__(self):
        return f"{self.user.username}: {self.text[:20]}"