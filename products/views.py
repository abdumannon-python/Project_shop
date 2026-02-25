from django.core.handlers.base import reset_urlconf
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import get_user_model
from .models import Products,Category,Wishlis,ProductImages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
User=get_user_model()


class ProductCreate(LoginRequiredMixin,View):
    def get(self,request):
        category=Category.objects.all()
        return render(request,'product_form.html',{'category':category})
    def post(self,request):
        category_id=request.POST.get('category')
        category=get_object_or_404(Category,id=category_id)
        percent_val=request.POST.get('percent')
        product=Products.objects.create(
            auth=request.user,
            category=category,
            title=request.POST.get('title'),
            brand=request.POST.get('brand'),
            price=request.POST.get('price'),
            percent=percent_val,
            main_image=request.FILES.get('main_image'),
            stock=request.POST.get('stock'),
            desc=request.POST.get('desc')
        )
        product.save()
        images=request.FILES.getlist('images')
        for imgage in images:
            ProductImages.objects.create(product=product,imgage=imgage)
        return redirect('dashboard')