from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import AbstractUser
from django.core.cache import cache
class User(AbstractUser):
    phone=models.CharField(max_length=15,null=True,blank=True)
    address=models.TextField(blank=True,null=True)
    email = models.EmailField(unique=True)
    profile_image = models.ImageField(upload_to='profile_image/', null=True, blank=True)
    balance = models.DecimalField(decimal_places=3, max_digits=10, null=True, blank=True)
    def __str__(self):
        return self.username

    @property
    def is_online(self):
        return cache.get(f"last-seen-{self.id}") is not None

    @property
    def last_seen(self):
        return cache.get(f"last-seen-{self.id}")


class Emailcode(models.Model):
    users=models.ForeignKey(User,on_delete=models.CASCADE,related_name='code')
    code=models.CharField(max_length=6)
    created_at=models.DateTimeField(auto_now_add=True)
    def is_valid(self):
        return timezone.now()<self.created_at+timedelta(minutes=2)
    def __str__(self):
        return f" {self.users.username} uchun kod {self.code}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment')
    post = models.ForeignKey('products.Products', on_delete=models.CASCADE, related_name='comment')
    text = models.TextField()