from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import get_user_model
from .models import *
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from orders.models import  OrderItem
from django.db.models import Sum
from users.models import *


User=get_user_model()


class ProductCreate(LoginRequiredMixin,View):
    def get(self,request):
        category=Category.objects.all()
        return render(request,'product_form.html',{'category':category})
                                                                        # category  da database dan kategoriyalar kealdi
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
                ProductImages.objects.create(product_id=pk, image=image)

        return redirect('dashboard')


class ProductDelete(LoginRequiredMixin,View):
    def get(self,request,pk):
        product=get_object_or_404(Products,pk=pk,auth=request.user)
        product.delete()
        return redirect('dashboard')


class ProductDetails(View):
    def get(self,request,pk):
        products=get_object_or_404(Products,pk=pk)
        category=Category.objects.filter(id=products.category).exclude(pk=pk)[:4]
        comment=Comment.objects.filter(prost_id=pk)
        last_week = timezone.now() - timedelta(days=7)
        order = OrderItem.objects.filter(product_id=pk,created_at__gte=last_week).exclude(order__status='cancelled')
        user_count=order.values('user').distinct().count()
        count_product=order.aggregate(total=Sum('quantity'))['total'] or 0
        context={
            'products':products,
            'comment':comment,
            'user_count':user_count,
            'count_product':count_product,
            'category':category
        }

        return render(request,'product_detail.html',context)

    def post(self, request, pk):
        post = get_object_or_404(Products, pk=pk)
        wishlist = get_object_or_404(Wishlist, user_id=request.user.id)

        if wishlist:
            wishlist.delete()
        else:
            Wishlist.objects.create(user=request.user, product=post)

        return redirect('product_detail')



class ProductView(View):
    def get(self,request):
        products=Products.objects.filter().order_by('category')
        return render(request,'index.html',{
            'products':products,
            })

class WishesView(View):
    def get(self, request, id):
        user = get_object_or_404(User, id = id)
        wish = Wishlist.objects.filter(user=user)
        return render(request, 'wishes.html',{
            "user": user,
            "wish": wish
        })



class Addwish(LoginRequiredMixin ,View):
    login_url = 'login'
    def post(self, request, id):
        post = get_object_or_404(Products, id = id)
        wishlis=get_object_or_404(Wishlist,user_id = request.user.id)

        if wishlis:
            wishlis.delete()
        else:
            Wishlist.objects.create(user=request.user,product=post)

        return redirect('home')


class ChatView(LoginRequiredMixin,View):
    def get(self,request):
        chats=Chat.objects.filter(participants=request.user).prefetch_related('participants').order_by('-created_at')

        context={
            'chats':chats
        }

        return render(request,'chat_list.html',context)

class ChatDetail(LoginRequiredMixin,View):
    def get(self,request,chat_id):
        chat=get_object_or_404(Chat,id=chat_id,participants=request.user)
        messages=chat.messages.all().order_by('created_at')
        recipient=chat.get_recipient(request.user)
        context = {
            'chat': chat,
            'messages': messages,
            'recipient': recipient
        }
        return render(request, 'chat_detail.html', context)

    def post(self,request,chat_id):
        chat=get_object_or_404(Chat,id=chat_id,participants=request.user)
        text = request.POST.get('text')
        image = request.FILES.get('image')

        if text or image:
            Messages.objects.create(
                user=request.user,
                chat=chat,
                text=text,
                image=image
            )
        return redirect('chat_detail', chat_id=chat.id)
class ChatCreate(LoginRequiredMixin,View):
    def get(self,request,recipient_id):
        chat=Chat.objects.filter(participants=request.user).filter(participants__id=recipient_id).first()

        if not chat:
            chat=Chat.objects.create()
            chat.participants.add(request.user,recipient_id)
            chat.save()

        return redirect('chat_detail', chat_id=chat.id)

class MessageUpdate(LoginRequiredMixin,View):
    def post(self,request,message_id):
        message=get_object_or_404(Messages,id=message_id,user=request.user)
        new_text = request.POST.get('text')

        if new_text:
            message.text=new_text
            message.save()
        return redirect('chat_detail',chat_id=message.chat.id)

class MessageDelete(LoginRequiredMixin,View):
    def post(self,request,message_id):
        message=get_object_or_404(Messages,id=message_id,user=request.user)
        message.delete()
        messages.success(request, "Xabar o‘chirildi")
        return redirect('chat_detail',chat_id=message.chat.id)


class ProductSearch(View):
    pass
