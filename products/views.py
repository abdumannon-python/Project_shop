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
        return redirect('/')
class ProductUpdate(LoginRequiredMixin,View):
    def get(self,request,pk):
        product=get_object_or_404(Products,pk=pk,auth=request.user)
        category=Category.objects.all()
        context={
            'product':product,
            'category':category
        }
        return render(request,'product_form.html',context)
    def post(self,request,pk):
        product = get_object_or_404(Products, pk=pk, auth=request.user)
        category_id = request.POST.get('category')
        category = get_object_or_404(Category, id=category_id)
        present_val = request.POST.get("present") or 0
        product.category_id=category
        product.title=request.POST.get('title')
        product.brand=request.POST.get('brand')
        product.price=request.POST.get('price')
        product.percent=present_val
        product.stock=request.POST.get('stock')
        product.desc=request.POST.get('desc')

        if request.FILES.get('main_image'):
            product.main_image = request.FILES.get('main_image')
        product.save()

        new_image=request.FILES.getlist('images')
        if new_image:
            ProductImages.objects.filter(product=product).delete()
            for image in new_image:
                ProductImages.objects.create(product=product, image=image)

        return redirect('/')
class ProductDelete(LoginRequiredMixin,View):
    def get(self,request,pk):
        product=get_object_or_404(Products,pk=pk,auth=request.user)
        product.delete()
        return redirect('/')
class ProductDetails(View):
    def get(self,request,pk):
        products=get_object_or_404(Products,pk=pk)








