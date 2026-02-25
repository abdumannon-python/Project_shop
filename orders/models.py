from django.db import models

from users.models import User
from products.models import Products


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Kutilmoqda'),
        ('processing', 'Jarayonda'),
        ('shipped', 'Yo‘lda'),
        ('delivered', 'Yetkazib berildi'),
        ('cancelled', 'Bekor qilindi'),
    ]

    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='orders')


    username=models.CharField(max_length=100,null=True,blank=True)
    phone=models.CharField(max_length=20,null=True,blank=True)
    address=models.TextField(null=True,blank=True)
    total_price=models.DecimalField(max_digits=10,decimal_places=2)

    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} --->{self.user.username}"

    class Meta:
        ordering=['-created_at']


class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='carts')
    is_ordered = models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} "

    @property
    def total_price(self):
        return sum(item.get_totel for item in self.items.all())


class CartItem(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='items')
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.title} --->{self.quantity} ta "
    @property
    def get_totel(self):
        price = self.product.discount_price if self.product.discount_price else self.product.price
        return price*self.quantity



class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        Products,
        on_delete=models.SET_NULL,
        null=True
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    product_title = models.CharField(max_length=200, blank=True)
    product_image = models.ImageField(upload_to='order_items/', null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.product:
            self.product_title = self.product.title
            if self.product.main_image:
                self.product_image = self.product.main_image
        super().save(*args, **kwargs)

    def __str__(self):
        title = self.product.title if self.product else self.product_title or "O'chirilgan mahsulot"
        return f"{title} x {self.quantity}"

    @property
    def get_total(self):
        return self.price * self.quantity




